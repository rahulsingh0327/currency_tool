import requests
from typing import Any, Dict


def _fetch_rates_exchangeratesapi(base: str = "USD") -> Dict[str, float]:
    """
    Fetch exchange rates from exchangerate.host (free, no API key needed).

    Args:
        base: Base currency code.

    Returns:
        Mapping from currency to rate relative to base.

    Raises:
        RuntimeError on network/parse error.
    """
    url = "https://api.exchangerate.host/latest"
    params = {"base": base}
    resp = requests.get(url, params=params, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"Currency API error: {resp.status_code} {resp.text}")
    data = resp.json()
    return data.get("rates", {})


@mcp.tool()
def currency_convert(amount: float, from_currency: str, to_currency: str, base_provider: str = "exchangerate.host") -> Dict[str, Any]:
    """
    Convert an amount from one currency to another using live rates.

    Args:
        amount: Numeric amount to convert.
        from_currency: ISO currency code, e.g., "USD".
        to_currency: ISO currency code, e.g., "INR".
        base_provider: Provider string; currently supports "exchangerate.host".

    Returns:
        Dict with original amount, converted amount, rate and provider raw info.

    Notes:
        This uses free exchangerate.host by default (no API key).
    """
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    rates = _fetch_rates_exchangeratesapi(base=from_currency)
    if to_currency not in rates:
        raise RuntimeError(f"Unsupported target currency or missing rate for {to_currency}")
    rate = rates[to_currency]
    converted = amount * rate
    return {"amount": amount, "from": from_currency, "to": to_currency, "rate": rate, "converted": converted}
