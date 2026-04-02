def test_signup_allows_exceeding_max_participants_current_behavior(client):
    # Arrange
    activity = "Debate Team"
    base_payload = client.get("/activities").json()[activity]
    max_participants = base_payload["max_participants"]

    seed_needed = max_participants - len(base_payload["participants"])
    for index in range(seed_needed):
        client.post(
            f"/activities/{activity}/signup",
            params={"email": f"seed{index}@mergington.edu"},
        )

    overflow_email = "overflow@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": overflow_email})

    # Assert
    assert response.status_code == 200
    participants = client.get("/activities").json()[activity]["participants"]
    assert len(participants) == max_participants + 1
    assert overflow_email in participants


def test_activity_name_is_case_sensitive(client):
    # Arrange
    activity = "chess club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_then_unregister_sequence_restores_participant_list(client):
    # Arrange
    activity = "Gym Class"
    email = "sequence.student@mergington.edu"
    before = client.get("/activities").json()[activity]["participants"]

    # Act
    signup_response = client.post(f"/activities/{activity}/signup", params={"email": email})
    unregister_response = client.delete(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200

    after = client.get("/activities").json()[activity]["participants"]
    assert after == before
