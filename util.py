import re

error_patterns = {
    r"401 Unauthorized|Authentication failed for package '@[\w-]+'|Unable to authenticate, invalid or missing authentication token": "Private Package Authentication Failure",
    r"npm error code E401|npm error Incorrect or missing password|npm error authentication token": "Private Package Authentication Failure",
    r"ERR! 404 Not Found|No matching version found for '([\w-]+)@([\d.x-]+)'|package ([\w-]+)@([\d.x-]+) not found in registry": "Unresolved Dependency",
    r"Conflicting dependencies found:[\s\S]*requires ([\w@.-]+) but ([\w@.-]+) is installed": "Dependency Version Conflict",
    r"npm ERR! Missing script: 'build'": "Incorrect Build Command Configuration",
    r"npm error Missing script: \"[\w-]+\"": "Incorrect Build Command Configuration",
    r"No build command configured, skipping dependency installation and build steps": "No Build Command Configured",
    r"Error: Missing required environment variable ([A-Z_]+)|Failed to load environment variables|is undefined": "Incorrect Environment Variables Configuration",
    r"destination of (rewrite|redirect) exceeds character limit of 512 characters": "Destination Exceeds Character Limit",
    r"launch.json error: length must be <= 512, but got \d+ at /rewrites/\d+/destination": "Destination Exceeds Character Limit",
    r"(rewrite|redirect) has no destination": "No Destination for Rewrite/Redirect",
    r"launch.json error: missing properties: 'destination' at /rewrites/\d+": "No Destination for Rewrite/Redirect",
    r"invalid regex in (rewrite|redirect)": "Invalid Regex in Rewrite/Redirect",
    r"launch.json error: rewrites has invalid Destination pattern": "Invalid Regex in Rewrite/Redirect",
    r"Edge functions deployment error": "Edge Function Deployment Error",
    r"Error while deleting user edge function": "Edge Function Deletion Error",
    r"Cloud function deployment failed|Unable to connect to the database during deployment": "Cloud Function Deployment Error",
    r"Cloud functions deployment error": "Cloud Function Deployment Error",
    r"Deployment failed during site setup": "Site Setup Deployment Failure",
    r"Deployment failed while setting up the site": "Site Setup Deployment Failure",
    r"SyntaxError: (.+) at (.+):(\d+):(\d+)": "Syntax Error",
    r"TypeError|ReferenceError|Uncaught Exception": "Runtime Error",
}

error_solutions = {
    "Private Package Authentication Failure": "Check your .npmrc file for the correct authentication token or login using 'npm login'. Ensure you have the necessary permissions to access the private package.",
    "Unresolved Dependency": "Ensure the package name and version are correct. Check if the package is deprecated or unavailable in the registry. Try clearing cache with 'npm cache clean --force'.",
    "Incorrect Build Command Configuration": "Ensure the 'build' script is defined in package.json under 'scripts'. Example: 'build': 'react-scripts build'.",
    "Incorrect Environment Variables Configuration": "Check if all required environment variables are set in the environment or in the .env file. Ensure no syntax errors like spaces around '='.",
    "Destination Exceeds Character Limit": "Shorten the destination URL to be within the 512 character limit. Consider using URL parameters instead of long query strings.",
    "No Destination for Rewrite/Redirect": "Ensure the 'destination' field is defined for the rewrite or redirect in launch.json.",
    "Invalid Regex in Rewrite/Redirect": "Check the regex pattern used in launch.json. Test it with an online regex validator to ensure it's valid.",
    "Edge Function Deletion Error": "Check for active deployments using the edge function. Ensure no dependencies are linked before deletion.",
    "Cloud Function Deployment Error": "Check the cloud function logs for more details. Verify the configuration and ensure all dependencies are installed.",
    "Site Setup Deployment Failure": "Verify the site setup configuration and permissions. Ensure all required resources are available.",
    "Syntax Error": "Check the file and line number mentioned. Fix any syntax errors in the code.",
    "Runtime Error": "Check the server logs for the full stack trace. Debug the code to handle the runtime exception.",
    "Private Package Authentication Failure": "Check your .npmrc file for the correct authentication token or login using 'npm login'. Ensure you have the necessary permissions to access the private package. If using CI/CD, verify environment variables for authentication.",
    "Incorrect Build Command Configuration": "Ensure the missing script is defined in package.json under 'scripts'. Verify the spelling and configuration of the build command.",
    "No Build Command Configured": "Define a build command in launch.json or package.json. Ensure the 'build' script is defined under 'scripts' in package.json.",
    "Destination Exceeds Character Limit": "Shorten the destination URL in launch.json to be within the 512 character limit. Consider using URL parameters or simplifying the path.",
    "No Destination for Rewrite/Redirect": "Ensure the 'destination' field is defined in launch.json for all rewrites or redirects. Refer to the documentation for proper syntax.",
    "Invalid Regex in Rewrite/Redirect": "Check the destination pattern in launch.json. Test the regex with an online validator to ensure it's valid. Review the Launch documentation for supported patterns.",
    "Edge Function Deployment Error": "Check the Edge Functions documentation for troubleshooting. Ensure the edge function is properly defined and does not exceed size limits. Check if dependencies are compatible with WinterCG.",
    "Cloud Function Deployment Error": "Check cloud function logs for more details. Verify the configuration, environment variables, and ensure all dependencies are installed.",
    "Site Setup Deployment Failure": "Verify site setup configuration and permissions. Ensure all required resources are available and properly configured.",
    "Dependency Version Conflict": "Check for version compatibility in package.json. Align the versions of conflicting packages. Use 'npm ls <package>' to see the dependency tree. After making changes, run 'npm install' or 'yarn install' to update the lockfile."
}

def classify_error(log_content):
    for pattern, error_type in error_patterns.items():
        if re.search(pattern, log_content):
            return error_type
    return "Unknown Error"

def get_solution(error_type):
    return error_solutions.get(error_type, "No solution available for this error.")

def read_log_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def extract_file(log_content):
    pattern = r"(/[\w./-]+\.js):\d+:\d+"
    file_paths = re.findall(pattern, log_content)
    
    if not file_paths:
        return "No file paths found in the log."
    
    outermost_file = file_paths[0]
    innermost_file = file_paths[-1]
    
    # return f"Outermost File: {outermost_file}, Innermost File: {innermost_file}"
    return f"Error Location: {outermost_file}"