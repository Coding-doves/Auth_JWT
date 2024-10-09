from fastapi import APIRouter
from app.models.post_model import PostSchema

posts = [
    {
        "id": 1,
        "title": "Herbert",
        "content": "This Herbert goes up down the street preaching."
    },
    {
        "id": 2,
        "title": "Ada",
        "content": "This Herbert goes up down the street preaching."
    },
    {
        "id": 3,
        "title": "Yesu",
        "content": "This Herbert goes up down the street preaching."
    }
]


router = APIRouter()


# Get/Post
@router.get("/posts")
def all_posts():
    return {"All Posts": posts}

# Get/Single Post
@router.get("/posts/{id}")
def specific_post(id: int):
    for post in posts:
        if post["id"] == id:
            return {f"Post with id-{id}": post}
    return {f"Post with id-{id}": "don't exist."}

# Post/Create Post
@router.post("/posts")
def create_posts(post: PostSchema):
    post_data = post.dict()
    post_data["id"] = len(posts) + 1
    posts.append(post_data)
    new_post = PostSchema(**post_data)

    return new_post
