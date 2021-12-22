from dataclasses import dataclass


@dataclass(init=True, repr=True)
class TokenAccount:
    url: str
    tokenUrl: str
    keyBookUrl: str
    balance: str
    txCount: int
    nonce: int
    creditBalance: str
