from marshmallow import Schema, fields, validate


class FlagEvaluationRequestSchema(Schema):

    flag_key = fields.String(
        required=True,
        validate=validate.Length(min=3, max=64),
        metadata={"description": "flag key to evaluate"},
    )

    user_context = fields.Dict(
        keys=fields.String(),
        values=fields.Raw(),
        load_default=dict,
        metadata={
            "description": "Context metrics (e.g., user_id, email) for targeting rules"
        },
    )


class FlagEvaluationResponseSchema(Schema):
    flag_key = fields.String(required=True)
    is_enabled = fields.Boolean(required=True)
    reason = fields.String(required=True)
    evaluated_at = fields.DateTime(required=True)
