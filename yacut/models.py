from __future__ import annotations

from datetime import datetime

from yacut import db


class URLMap(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)  # type: ignore[assignment]
    original: str = db.Column(db.String(2048), nullable=False)  # type: ignore[assignment]
    short: str = db.Column(db.String(16), unique=True, nullable=False)  # type: ignore[assignment]
    timestamp: datetime = db.Column(  # type: ignore[assignment]
        db.DateTime, index=True, default=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f'<URLMap {self.short} -> {self.original[:60]}...>'
