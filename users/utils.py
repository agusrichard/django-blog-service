from dataclasses import dataclass

RELATIONSHIP_FOLLOWING = 1
RELATIONSHIP_BLOCKED = 2
RELATIONSHIP_STATUSES = (
    (RELATIONSHIP_FOLLOWING, "Following"),
    (RELATIONSHIP_BLOCKED, "Blocked"),
)


@dataclass
class RelationshipActions:
    FOLLOW = "FOLLOW"
    BLOCK = "BLOCK"
    UNFOLLOW = "UNFOLLOW"
    UNBLOCK = "UNBLOCK"
