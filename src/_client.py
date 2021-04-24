from typing import Optional, List, Callable

import requests

from src._models import WallGetResponse


class VkWallHandler:
    API_URL = "https://api.vk.com/method/"
    VERSION: str = "5.52"

    def __init__(self, access_token: str):
        self.access_token = access_token

    def get(
            self,
            owner_id: int,
            domain: Optional[str] = None,
            offset: Optional[int] = None,
            filter_: Optional[str] = None,
            count: Optional[int] = None,
    ) -> WallGetResponse:
        method = "/wall.get"
        response = requests.get(
                self.API_URL + method,
                params=self._get_query(
                    owner_id=owner_id,
                    domain=domain,
                    offset=offset,
                    filter=filter_,
                    count=count
                )
            )
        response_json: dict = response.json()
        return WallGetResponse(**response_json)

    def delete(self, owner_id: int, post_id: int) -> bool:
        method = "/wall.delete"
        response = requests.get(
                self.API_URL + method,
                params=self._get_query(
                    owner_id=owner_id,
                    post_id=post_id
                )
            )
        result = response.json().get("response")
        if result == 1:
            return True
        return False

    def clear_wall(
            self,
            owner_id: int,
            whose_posts: str = "all",
            filters: Optional[List[Callable]] = None,
            step: int = 100
    ):
        posts_to_delete: set = set()
        offset: int = 0
        while True:
            response: WallGetResponse = self.get(
                owner_id,
                filter_=whose_posts,
                count=step,
                offset=offset
            )
            offset += step
            if not response.response or not response.response.items:
                break
            for item in response.response.items:
                if not item.can_delete:
                    continue
                if not filters:
                    posts_to_delete.add(item.id)
                    continue
                if any(filter_(item) for filter_ in filters):
                    posts_to_delete.add(item.id)

        continue_: str = input(f"There are {len(posts_to_delete)} posts to delete! Continue (Y/N)?")
        if continue_.strip().lower() != "y":
            exit(1)

        while posts_to_delete:
            post_id: int = posts_to_delete.pop()
            deleted: bool = self.delete(owner_id, post_id)
            if deleted:
                print(f"Post {post_id} deleted!")
            else:
                posts_to_delete.add(post_id)

    def _get_query(self, **kwargs) -> dict:
        """ Create query with common params for all methods """
        query = dict(
            access_token=self.access_token,
            v=self.VERSION
        )
        query.update(kwargs)
        return query
