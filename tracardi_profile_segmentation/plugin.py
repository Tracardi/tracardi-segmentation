from tracardi.domain.profile import Profile
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi_plugin_sdk.domain.result import Result
from tracardi.process_engine.tql.condition import Condition
from tracardi_profile_segmentation.model.configuration import Configuration


def validate(config: dict):
    return Configuration(**config)


class ProfileSegmentAction(ActionRunner):

    def __init__(self, **kwargs):
        self.config = validate(kwargs)

    async def run(self, payload):
        dot = self._get_dot_accessor(payload)
        condition = Condition()
        if await condition.evaluate(self.config.condition, dot):
            profile = Profile(**dot.profile)
            if self.config.action.lower() == 'add':
                if self.config.segment not in profile.segments:
                    profile.segments.append(self.config.segment)
            else:
                if self.config.segment in profile.segments:
                    profile.segments.remove(self.config.segment)

            self.profile.replace(profile)

        return Result(port="payload", value=payload)


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_profile_segmentation.plugin',
            className='ProfileSegmentAction',
            inputs=["payload"],
            outputs=['payload'],
            version='0.6.0',
            license="MIT",
            author="Risto Kowaczewski",
            init={
                "segment": "",
                "action": "add",  # the default action (we have add and remove to choose form)
                "condition": ""
            },
            form=Form(groups=[
                FormGroup(
                    name="Add or remove segment",
                    description="Set the conditions for profile segmentation.",
                    fields=[
                        FormField(
                            id="segment",
                            name="Segment name",
                            description="Provide segment name. This name will be used to mark a profile. "
                                        "Please use dashes instead of spaces.",
                            component=FormComponent(type="text", props={"label": "segment"})
                        ),
                        FormField(
                            id="action",
                            name="What would you like to do",
                            description="Please select either to ADD or REMOVE the segment.",
                            component=FormComponent(type="select", props={"label": "action", "items": {
                                "add": "Add segment",
                                "remove": "Remove segment"
                            }})
                        ),
                        FormField(
                            id="condition",
                            name="Condition statement",
                            description="Provide condition for segmentation. If the condition is met then the profile "
                                        "will be segmented to defined segment.",
                            component=FormComponent(type="textarea", props={"label": "condition"})
                        )
                    ]
                ),
            ]),
        ),
        metadata=MetaData(
            name='Add/Remove segment',
            desc='This plugin will add/remove segment from the profile.',
            type='flowNode',
            width=200,
            height=100,
            icon='group-person',
            group=["Data processing"]
        )
    )
