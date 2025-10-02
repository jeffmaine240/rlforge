import pytest

BASE_URL = "/api/v1/environments"


@pytest.mark.asyncio
async def test_environment_crud(async_test_client):
    client = async_test_client

    # ------------------------------
    # CREATE ENVIRONMENT
    # ------------------------------
    create_resp = await client.post(
        BASE_URL,
        json={"name": "TestEnv", "env_id": "CartPole-v1"}
    )
    assert create_resp.status_code == 200, create_resp.text
    env_data = create_resp.json()
    assert env_data["name"] == "TestEnv"

    # ------------------------------
    # STEP ENVIRONMENT
    # ------------------------------
    step_resp = await client.post(
        f"{BASE_URL}/TestEnv/step",
        json={"action": 0}  # ❗ Provide required body
    )
    assert step_resp.status_code == 200, step_resp.text
    step_data = step_resp.json()
    assert "observation" in step_data
    assert "reward" in step_data

    # ------------------------------
    # RESET ENVIRONMENT
    # ------------------------------
    reset_resp = await client.post(f"{BASE_URL}/TestEnv/reset")
    assert reset_resp.status_code == 200, reset_resp.text
    reset_data = reset_resp.json()
    assert "observation" in reset_data

    # ------------------------------
    # DELETE ENVIRONMENT
    # ------------------------------
    delete_resp = await client.delete(f"{BASE_URL}/TestEnv")
    assert delete_resp.status_code == 200, delete_resp.text
    delete_data = delete_resp.json()
    assert delete_data["message"] == "Environment 'TestEnv' deleted successfully."
