import requests
import simple_salesforce
from ruxit.api.base_plugin import RemoteBasePlugin
import logging

logger = logging.getLogger(__name__)

class SalesforceLimitsPlugin(RemoteBasePlugin):
    def initialize(self, **kwargs):
        self.username = self.config["username"]
        self.password = self.config["password"]
        self.organizationId = self.config["organizationId"]
        self.domain = self.config["domain"]
        self.api_url = self.config["apiURL"]

        if self.domain == '':
            self.salesforce_instance = simple_salesforce.Salesforce(username=self.username, password=self.password, organizationId=self.organizationId)

        else:
            self.salesforce_instance = simple_salesforce.Salesforce(username=self.username, password=self.password, organizationId=self.organizationId, domain=self.domain)

        logger.info("initialization complete")

    def query(self, **kwargs):
        limits = requests.get(self.api_url, timeout=10, headers=self.salesforce_instance.headers).json()
        group_name = "salesforce_group"
        group = self.topology_builder.create_group(group_name, group_name)
        device_name = "salesforce_instance"
        device = group.create_device(device_name, device_name)
        logger.info("Topology: group name=%s, device name=%s", group.name, device.name)
        #Single email
        device.absolute(key='single_email_max', value=limits["SingleEmail"]["Max"])
        device.absolute(key='single_email_remaining', value=limits["SingleEmail"]["Remaining"])
        device.absolute(key='single_email_percentage', value=limits["SingleEmail"]["Remaining"]/limits["SingleEmail"]["Max"]*100)
        # Daily Api Requests
        device.absolute(key='daily_api_requests_max', value=limits["DailyApiRequests"]["Max"])
        device.absolute(key='daily_api_requests_remaining', value=limits["DailyApiRequests"]["Remaining"])
        device.absolute(key='daily_api_requests_percentage', value=limits["DailyApiRequests"]["Remaining"]/limits["DailyApiRequests"]["Max"]*100)
        # Daily Async Apex Executions
        device.absolute(key='daily_async_apex_executions_max', value=limits["DailyAsyncApexExecutions"]["Max"])
        device.absolute(key='daily_async_apex_executions_remaining', value=limits["DailyAsyncApexExecutions"]["Remaining"])
        device.absolute(key='daily_async_apex_executions_percentage', value=limits["DailyAsyncApexExecutions"]["Remaining"]/limits["DailyAsyncApexExecutions"]["Max"]*100)
        # Daily Bulk Api Batches
        device.absolute(key='daily_bulk_api_batches_max', value=limits["DailyBulkApiBatches"]["Max"])
        device.absolute(key='daily_bulk_api_batches_remaining', value=limits["DailyBulkApiBatches"]["Remaining"])
        device.absolute(key='daily_bulk_api_batches_percentage', value=limits["DailyBulkApiBatches"]["Remaining"]/limits["DailyBulkApiBatches"]["Max"]*100)
        # Daily Durable Generic Streaming Api Event
        device.absolute(key='daily_durable_generic_streaming_api_events_max', value=limits["DailyDurableGenericStreamingApiEvents"]["Max"])
        device.absolute(key='daily_durable_generic_streaming_api_events_remaining', value=limits["DailyDurableGenericStreamingApiEvents"]["Remaining"])
        device.absolute(key='daily_durable_generic_streaming_api_events_percentage', value=limits["DailyDurableGenericStreamingApiEvents"]["Remaining"]/limits["DailyDurableGenericStreamingApiEvents"]["Max"]*100)
        # Data Storage
        device.absolute(key='data_storage_mb_max', value=limits["DataStorageMB"]["Max"])
        device.absolute(key='data_storage_mb_remaining', value=limits["DataStorageMB"]["Remaining"])
        device.absolute(key='data_storage_mb_percentage', value=limits["DataStorageMB"]["Remaining"]/limits["DataStorageMB"]["Max"]*100)
        # Durable Streaming Api Concurrent Clients
        device.absolute(key='durable_streaming_api_concurrent_clients_max', value=limits["DurableStreamingApiConcurrentClients"]["Max"])
        device.absolute(key='durable_streaming_api_concurrent_clients_remaining', value=limits["DurableStreamingApiConcurrentClients"]["Remaining"])
        device.absolute(key='durable_streaming_api_concurrent_clients_percentage', value=limits["DurableStreamingApiConcurrentClients"]["Remaining"]/limits["DurableStreamingApiConcurrentClients"]["Max"]*100)
        # Hourly Time Based Workflow
        device.absolute(key='hourly_time_based_workflow_max', value=limits["HourlyTimeBasedWorkflow"]["Max"])
        device.absolute(key='hourly_time_based_workflow_remaining', value=limits["HourlyTimeBasedWorkflow"]["Remaining"])
        device.absolute(key='hourly_time_based_workflow_percentage', value=limits["HourlyTimeBasedWorkflow"]["Remaining"]/limits["HourlyTimeBasedWorkflow"]["Max"]*100)
        # Permission Sets
        device.absolute(key='permission_sets_max', value=limits["PermissionSets"]["Max"])
        device.absolute(key='permission_sets_remaining', value=limits["PermissionSets"]["Remaining"])
        device.absolute(key='permission_sets_percentage', value=limits["PermissionSets"]["Remaining"]/limits["PermissionSets"]["Remaining"]*100)
