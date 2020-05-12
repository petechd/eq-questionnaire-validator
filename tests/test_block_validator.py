from app.validation import error_messages
from app.validation.blocks import BlockValidator
from app.validation.questionnaire_schema import QuestionnaireSchema


def test_invalid_reference():
    known_identifiers = ["answer-1", "answer-2"]

    questionnaire_schema = QuestionnaireSchema({})
    validator = BlockValidator({"id": "block-1"}, questionnaire_schema)
    validator.questionnaire_schema.answers_with_context = {
        "answer-1": {
            "answer": {
                "decimal_places": 2,
                "id": "answer-1",
                "label": "Answer 1",
                "mandatory": False,
                "type": "Number",
            },
            "block": "block-1",
        }
    }

    validator.validate_answer_source_reference(
        identifiers=known_identifiers, current_block_id="block-1"
    )

    expected_errors = [
        {
            "message": error_messages.ANSWER_SELF_REFERENCE,
            "referenced_id": "answer-1",
            "block_id": "block-1",
        },
        {
            "message": error_messages.ANSWER_REFERENCE_INVALID,
            "referenced_id": "answer-2",
            "block_id": "block-1",
        },
    ]
    assert validator.errors == expected_errors
