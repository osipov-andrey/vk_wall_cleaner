from datetime import datetime
from typing import List, Union, Optional

from pydantic import BaseModel


class Reports(BaseModel):
    count: int
    wall_count: int
    mail_count: int
    user_reposted: int


class Likes(BaseModel):
    count: int
    user_likes: int
    can_like: int
    can_publish: int


class Comments(BaseModel):
    count: int
    can_post: int
    groups_can_post: bool


class PostSource(BaseModel):
    type: str
    platform: Optional[str] = None


class Item(BaseModel):
    id: int
    from_id: int
    owner_id: int
    date: Union[datetime, int]
    post_type: str
    text: str
    can_delete: int
    can_pin: Optional[int] = None
    is_pinned: Optional[int] = None
    can_archive: bool
    is_archived: bool
    post_source: PostSource
    comments: Comments
    likes: Likes
    reposts: Reports

    def __post_init_post_validate__(self, **kwargs):
        super().__init__(**kwargs)
        self.date = datetime.fromtimestamp(self.date)


class Response(BaseModel):
    count: int
    items: List[Item]


class WallGetResponse(BaseModel):
    response: Optional[Response] = None
