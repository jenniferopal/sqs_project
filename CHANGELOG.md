# Changelog

## [1.0.0] - 2025-07-11

### Added
- Complete working SQS monitoring script (main_sqs_queues.py)
- Enhanced CLI functionality with proper queue name and message count display
- Comprehensive error handling and script reliability
- Retroactive CHANGELOG has been added.

### Changed
- Major refactoring from sqs_queues.py to main_sqs_queues.py for improved stability
- Updated README documentation to reflect current functionality
- Improved script architecture for better maintainability

### Fixed
- Resolved script execution failures and get_queue_messages function issues
- Fixed queue name extraction and message counting logic

### Removed
- Removed problematic sqs_queues.py implementation

## [0.8.0] - 2025-07-11

### Added
- Separate functions for handling messages with and without DLQ
- Enhanced main() function for cleaner reuse and CLI operations
- Improved code modularity and organization

### Changed
- Restructured function architecture for better separation of concerns

## [0.7.0] - 2025-07-10

### Added
- Comprehensive test coverage for script operations

### Changed
- Reorganised project file structure

## [0.6.0] - 2025-07-10

### Added
- Complete project documentation with README
- Usage instructions for both Terraform module and Python script
- Setup and configuration guidelines

### Changed
- Restructured repository layout - moved Terraform files to root level
- Improved project organization for better accessibility

### Fixed
- Corrected string extraction for dictionary operations
- Fixed queue_name loop logic for proper iteration

## [0.5.0] - 2025-07-10

### Added
- SQS message counting functionality
- Queue name and message count display
- Basic script output formatting

### Fixed
- Improved script output to properly display queue information

## [0.4.0] - 2025-07-09

### Added
- Python script for fetching and displaying SQS message totals
- CLI testing and result printing functionality
- Module outputs for queue ARNs

### Fixed
- Corrected main queue resource configuration
- Added missing variables for successful execution

## [0.3.0] - 2025-07-09

### Added
- IAM roles creation with create_roles boolean variable
- Consumer and producer IAM roles with proper assume role policies
- Enhanced module flexibility with optional role creation

### Fixed
- Corrected IAM service references
- Fixed create_roles variable type and default value

## [0.2.0] - 2025-07-09

### Added
- IAM policies for SQS operations (send, receive, delete messages)
- Module outputs for policy and queue ARNs
- Terraform configuration with proper version constraints
- .gitignore for security and state management
- Terraform lock file for dependency management

### Changed
- Removed hardcoded AWS provider configuration following Terraform best practices
- Updated version compatibility requirements for AWS provider and Terraform

### Fixed
- Corrected Terraform and AWS provider version specifications

## [0.1.0] - 2025-07-08

### Added
- Initial Terraform module structure for SQS queues
- Dead letter queue (DLQ) configuration with automatic attachment
- Module variables for queue names and AWS region
- SQS queue creation with DLQ suffix naming convention
- Basic module framework with variables, outputs, and versions files
- GitHub Actions workflow for automatic changelog generation using release-drafter

### Infrastructure
- Created foundational module structure
- Established naming conventions for queues and dead letter queues
- Set up automated release management

---

## Notes

This changelog was created retroactively based on detailed git commit history spanning the complete development lifecycle from initial setup to production-ready release.