import dataiku
import os
import time
from dataiku.scenario import Scenario

# Function to check if the deployment JSON file exists
def is_deployment_json_removed(deployment_id):
    deployment_path = f"/opt/dataiku/dss/config/api-deployer/deployments/{deployment_id}.json"
    return not os.path.exists(deployment_path)

# Function to safely remove the deployment JSON file if it exists
def remove_deployment_json(deployment_id):
    deployment_path = f"/opt/dataiku/dss/config/api-deployer/deployments/{deployment_id}.json"
    if os.path.exists(deployment_path):
        try:
            os.remove(deployment_path)
            print(f"Removed residual deployment JSON: {deployment_path}")
        except Exception as e:
            print(f"Failed to remove {deployment_path}: {e}")

def create_or_update_deployment(api_service_name, service_id, deployment_id, version):
    """
    Create or update an API deployment with the given details.
    """
    slb_client = dataiku.api_client()
    apideployer = slb_client.get_apideployer()
    project = slb_client.get_project(dataiku.default_project_key())
    api_infrastructure_id = apideployer.list_infras()[0].id

    # Get the API service
    api_service = project.get_api_service(api_service_name)
    assert api_service.get_settings(), f"Service {api_service} not found"

    # Check if the package with the given version exists
    existing_packages = api_service.list_packages()
    package_exists = any(item['id'] == version for item in existing_packages)

    if not package_exists:
        print(f"Creating Version {version}...")
        api_service.create_package(version)

    if not apideployer.get_service(service_id):
        print(f"Creating Service {service_id}...")
        apideployer.create_service(service_id)

    try:
        print(f"Publishing package {version} to {service_id}...")
        api_service.publish_package(version, service_id)
    except Exception as e:
        print(f"Version {version} already exists for this published API: {e}")

    try:
        deployment = apideployer.get_deployment(deployment_id)
        deployment_status = deployment.get_status().get_health()
        print(f"Deployment status: {deployment_status}")

        if deployment_status != "HEALTHY":
            deployment = None
    except Exception as e:
        print(f"Deployment {deployment_id} is corrupted: {e}")
        deployment = None

    if deployment is None:
        print(f"Deploying {deployment_id}...")
        deployment = apideployer.create_deployment(
            deployment_id,
            service_id,
            api_infrastructure_id,
            version
        )

    # Start and wait for the deployment update
    deployment.start_update().wait_for_result()

def clean_up(api_service_name, service_id, deployment_id, version):
    """
    Delete API deployment, API service package, and service based on provided details.
    """
    slb_client = dataiku.api_client()
    apideployer = slb_client.get_apideployer()
    project = slb_client.get_project(dataiku.default_project_key())

    def delete_with_error_handling(delete_function, entity_name):
        try:
            delete_function()
        except Exception as error:
            print(f"Error deleting {entity_name}: {error}")

    # Safely remove deployment and ensure its JSON file is removed
    def delete_and_confirm(apideployer, deployment_id):
        delete_deployment(apideployer, deployment_id)
        for attempt in range(5):  # Retry for up to 5 times
            if is_deployment_json_removed(deployment_id):
                print(f"Deployment {deployment_id} successfully deleted.")
                return True
            time.sleep(2)  # Wait for 2 seconds before retrying
        print(f"Failed to delete deployment {deployment_id} after 5 attempts.")
        return False

    delete_with_error_handling(lambda: delete_and_confirm(apideployer, deployment_id), "deployment")
    delete_with_error_handling(lambda: project.get_api_service(api_service_name).delete_package(version), "API service package")
    delete_with_error_handling(lambda: apideployer.get_service(service_id).delete(), "service")

    # Double-check if JSON file exists, and remove if necessary
    remove_deployment_json(deployment_id)

def delete_deployment(apideployer, deployment_id):
    """
    Disables and deletes a deployment with proper cleanup.
    """
    deployment = apideployer.get_deployment(deployment_id)
    deployment_settings = deployment.get_settings()
    deployment_settings.set_enabled(False)
    deployment_settings.save(ignore_warnings=True)
    deployment.start_update().wait_for_result()  # Update the deployment to disable it
    deployment.delete(ignore_pre_delete_errors=True)

def main():
    # Define API deployment details
    api_service_name = "apiservice"
    service_id = "apitestservice"
    deployment_id = "apitestdeployment"
    version = "v1"

    # Create or update the deployment
    create_or_update_deployment(api_service_name, service_id, deployment_id, version)

    # Set scenario variables and cleanup
    scenario = Scenario()
    clean_up(api_service_name, service_id, deployment_id, version)

main()
