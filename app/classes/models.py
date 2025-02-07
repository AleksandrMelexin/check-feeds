from datetime import datetime, timezone

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, WriteOnlyMapped

import app


class Feeds(app.db.Model):
    __tablename__ = "feeds"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    url: Mapped[str] = mapped_column(unique=False)
    date_check: Mapped[datetime] = mapped_column(index=False, default=lambda: datetime.now(timezone.utc))
    check_feeds: WriteOnlyMapped['CheckFeeds'] = relationship(back_populates='feeds')


class CheckFeeds(app.db.Model):
    __tablename__ = "check_results"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    feed_id: Mapped[int] = mapped_column(ForeignKey(Feeds.id))
    picture_error_count: Mapped[int] = mapped_column(unique=False)
    name_error_count: Mapped[int] = mapped_column(unique=False)
    id_error_count: Mapped[int] = mapped_column(unique=False)
    feeds: Mapped[Feeds] = relationship(back_populates='check_feeds')
