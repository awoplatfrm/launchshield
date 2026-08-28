from datetime import datetime, timezone
from marshmallow import ValidationError
from flask import request, jsonify, Blueprint

from app.schemas.flags import FlagEvaluationRequestSchema, FlagEvaluationResponseSchema
from app.models.tenants import db
from app.models.flags import FeatureFlag
from sqlalchemy import select

api_bp = Blueprint("evaluate", __name__)


eval_request_schema = FlagEvaluationRequestSchema()
eval_resonse_schema = FlagEvaluationResponseSchema()


@api_bp.route("/evaluate", methods=["POST"])
def evaluate():
    json_payload = request.get_json()
    if not json_payload:
        return jsonify({"error": "invalid or missing payload"}), 400

    try:
        data = eval_request_schema.load(json_payload)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 422

    flag_key = data["flag_key"]

    tenant_id = request.headers.get("X-Tenant-ID")

    if not tenant_id:
        return jsonify({"error": "X-Tenant_ID missing"}), 401

    flag = db.session.execute(
        select(FeatureFlag).where(
            FeatureFlag.tenant_id == tenant_id, FeatureFlag.key == flag_key
        )
    ).scalar_one_or_none()

    if not flag:
        response_payload = {
            "flag_key": flag_key,
            "is_enabled": False,
            "reason": "FLAG NOT FOUND DEFAULT OFF",
            "evaluated_time": datetime.now(timezone.utc),
        }
    else:
        response_payload = {
            "flag_key": flag_key,
            "is_enabled": flag.is_enabled,
            "reason": "MATCHED_STATIC_RULE",
            "evaluated_time": datetime.now(timezone.utc),
        }

    return jsonify(eval_resonse_schema.dump(response_payload)), 200
