from datetime import datetime

from src._client import VkWallHandler


APP_ID = "7820734"
API_VER = "5.13"

OAUTH_URL = f"https://oauth.vk.com/authorize?client_id={APP_ID}" \
            f"&display=page" \
            f"&redirect_uri=http://vk.com&scope=wall" \
            f"&response_type=token" \
            f"&v={API_VER}0" \
            f"&state=123456"


def main():
    print("How to get access Token:\n".upper())
    print("Input URL in yor browser, authorize and copy access_token "
          "and User_ID from redirect URL (see in address bar): \n")
    print(OAUTH_URL)
    print("\n")

    access_token = input("Input access token: ")
    owner_id = int(input("Input wall owner ID: "))

    print("-" * 20)
    print("Filters for delete (input or press Enter with empty field): \n")

    contains_text = input("Contains text: ").lower().strip()
    not_contains_text = input("NOT contains text: ").lower().strip()
    from_date = input("From date (%Y %m %d): ")
    if from_date:
        from_date = datetime.strptime(from_date, "%Y %m %d")
    to_date = input("From date (%Y %m %d): ")
    if to_date:
        to_date = datetime.strptime(to_date, "%Y %m %d")

    delete_pinned = input("Delete pinned: ")

    whose_posts = input("Whose posts (owner/others/all): ")

    filters = list()
    # All filters are work with _models.Item
    if contains_text:
        filters.append(lambda x: contains_text in x.text.lower())
    if not_contains_text:
        filters.append(lambda x: contains_text not in x.text.lower())
    if from_date:
        filters.append(lambda x: x.date >= from_date)
    if to_date:
        filters.append(lambda x: x.date <= from_date)
    if not delete_pinned:
        filters.append(lambda x: not x.is_pinned)

    client = VkWallHandler(access_token)
    client.clear_wall(
        owner_id,
        whose_posts=whose_posts if whose_posts else "all"
    )


if __name__ == '__main__':
    main()
