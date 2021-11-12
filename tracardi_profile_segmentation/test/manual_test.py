from tracardi.domain.context import Context
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.profile import Profile
from tracardi.domain.profile_stats import ProfileStats
from tracardi.domain.session import Session
from tracardi_plugin_sdk.service.plugin_runner import run_plugin

from tracardi_profile_segmentation.plugin import ProfileSegmentAction

init = {
  "segment": "frequent-user",
  "action": "add",
  "condition": "profile@stats.visits>10"
}
payload = {}
profile = Profile(id="profile-id", stats=ProfileStats(visits=20))
event = Event(id="event-id",
              type="event-type",
              profile=profile,
              session=Session(id="session-id"),
              source=Entity(id="source-id"),
              context=Context())
result = run_plugin(ProfileSegmentAction, init, payload,
                    profile)

assert "frequent-user" in result.profile.segments
print("OUTPUT:", result.output)
print("PROFILE:", result.profile)
