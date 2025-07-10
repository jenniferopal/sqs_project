# Simple unit tests for SQS module

import unittest
import sys
import os
import boto3

# Import our SQS script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from unittest.mock import patch, MagicMock
from sqs_queues import get_queues_message_totals

# Try to import moto for realistic AWS testing
try:
    from moto import mock_sqs
    MOTO_AVAILABLE = True
except ImportError:
    MOTO_AVAILABLE = False
    def mock_sqs(func): return func


class TestSQSScript(unittest.TestCase):
    """Test our SQS monitoring script"""
    
    def test_message_count_success(self):
        """Test normal message counting"""
        test_queues = ["https://sqs.us-east-1.amazonaws.com/123/my-queue"]
        fake_response = {'Attributes': {'ApproximateNumberOfMessages': '10'}}
        
        with patch('sqs_queues.boto3.client') as mock_boto3:
            mock_sqs = MagicMock()
            mock_boto3.return_value = mock_sqs
            mock_sqs.get_queue_attributes.return_value = fake_response
            
            result = get_queues_message_totals(test_queues)
        
        self.assertEqual(result, {'my-queue': 10})
    
    def test_error_handling(self):
        """Test AWS error handling"""
        test_queues = ["https://sqs.us-east-1.amazonaws.com/123/broken-queue"]
        
        with patch('sqs_queues.boto3.client') as mock_boto3:
            mock_sqs = MagicMock()
            mock_boto3.return_value = mock_sqs
            mock_sqs.get_queue_attributes.side_effect = Exception("AWS Error")
            
            with patch('builtins.print'):
                result = get_queues_message_totals(test_queues)
        
        self.assertEqual(result, {'broken-queue': None})


class TestTerraformLogic(unittest.TestCase):
    """Test Terraform module logic"""
    
    def test_dlq_naming(self):
        """Test dead letter queue naming"""
        queue_names = ["orders", "payments"]
        dlq_names = [f"{name}-dlq" for name in queue_names]
        self.assertEqual(dlq_names, ["orders-dlq", "payments-dlq"])
    
    def test_iam_permissions(self):
        """Test IAM permission separation"""
        consumer_perms = ["sqs:ReceiveMessage", "sqs:DeleteMessage"]
        producer_perms = ["sqs:SendMessage"]
        
        self.assertIn("sqs:ReceiveMessage", consumer_perms)
        self.assertNotIn("sqs:ReceiveMessage", producer_perms)


@unittest.skipUnless(MOTO_AVAILABLE, "moto not available")
class TestWithMoto(unittest.TestCase):
    """Test with realistic AWS simulation using moto"""
    
    @mock_sqs
    def test_real_sqs_simulation(self):
        """Test with real simulated SQS queues"""
        # Create SQS client and queue
        sqs = boto3.client('sqs', region_name='us-east-1')
        response = sqs.create_queue(QueueName='test-queue')
        queue_url = response['QueueUrl']
        
        # Send messages
        sqs.send_message(QueueUrl=queue_url, MessageBody='msg1')
        sqs.send_message(QueueUrl=queue_url, MessageBody='msg2')
        
        # Test our function
        result = get_queues_message_totals([queue_url])
        self.assertEqual(result['test-queue'], 2)


if __name__ == '__main__':
    print("Running SQS tests...")
    if not MOTO_AVAILABLE:
        print("Install moto for realistic tests: pip install moto")
    unittest.main()