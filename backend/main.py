from typing import Optional

from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


# ----------------------------------------------------------------------
# Existing demo endpoints (keep them – they’re harmless)
# ----------------------------------------------------------------------
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}


# ----------------------------------------------------------------------
# NEW: Stock‑price endpoint for ticker ATYR
# ----------------------------------------------------------------------
STOCK_TOOL_URL = "http://localhost:8000"  # Render will route internally; keep same host/port


def _call_stock_tool(symbol: str) -> float:
    """
    Calls Render’s built‑in `stock` tool (exposed as a local HTTP endpoint)
    and extracts the current price.

    The tool expects a JSON payload:
        { "symbol": "<ticker>", "days": null }

    It returns a JSON document that looks like:
        {
            "symbol": "ATYR",
            "price": 12.34,
            "currency": "USD",
            "timestamp": "2025-09-27T14:32:10Z",
            ...
        }

    If the tool fails or the response shape changes we raise an HTTPException
    so the API consumer gets a clear 502/500 error.
    """
    payload = {"symbol": symbol, "days": None}
    try:
        # The stock tool is exposed as a function endpoint inside the same container.
        # Render automatically maps function names to `/functions/<name>` – the
        # exact path is documented in the Render UI. For this example we use
        # the generic `/functions/stock` endpoint.
        resp = requests.post(
            f"{STOCK_TOOL_URL}/functions/stock",
            json=payload,
            timeout=5,
        )
        resp.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to reach stock tool: {exc}",
        ) from exc

    data = resp.json()
    # Defensive: make sure the key we need exists
    if "price" not in data:
        raise HTTPException(
            status_code=502,
            detail="Stock tool response missing `price` field",
        )
    return float(data["price"])


@app.get("/price/ATYR")
def get_atyr_price():
    """
    Returns the latest market price for ATYR.
    The response format mirrors the raw tool output but stripped down to the
    fields most callers need.
    """
    price = _call_stock_tool("ATYR")
    return {
        "symbol": "ATYR",
        "price": price,
        "currency": "USD",  # the stock tool always returns USD for US equities
    }