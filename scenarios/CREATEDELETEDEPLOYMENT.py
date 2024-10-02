import dataiku
import time
from dataiku.scenario import Scenario


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
        
    if not apideployer.get_deployment(deployment_id):
        print(f"Creating deployment {deployment_id}...")
        apideployer.create_deployment(deployment_id)

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

    delete_with_error_handling(lambda: delete_deployment(apideployer, deployment_id), "deployment")
    delete_with_error_handling(lambda: project.get_api_service(api_service_name).delete_package(version), "API service package")
    delete_with_error_handling(lambda: apideployer.get_service(service_id).delete(), "service")


def delete_deployment(apideployer, deployment_id):
    deployment = apideployer.get_deployment(deployment_id)
    deployment_settings = deployment.get_settings()
    deployment_settings.set_enabled(False)
    deployment_settings.save(ignore_warnings=True)
    deployment.start_update().wait_for_result() # Update the deployment to disable it
    deployment.delete(ignore_pre_delete_errors=True)



def main():
    # Define API deployment details
    api_service_name = "myservice"
    service_id = "mytestservice"
    deployment_id = "mytestdeployment"
    version = "v1"

    # Create or update the deployment
    create_or_update_deployment(api_service_name, service_id, deployment_id, version)

    # Set scenario variables
    scenario = Scenario()
    clean_up(api_service_name, service_id, deployment_id, version)


main()

