
import vanna as vn
import logging
import os

logger = logging.getLogger(__name__)

def setup_vanna_api():
    """Setup Vanna API key"""
    try:
        # Check if API key exists in environment
        api_key = os.environ.get("VANNA_API_KEY")
        if not api_key:
            logger.info("No API key found, requesting new one...")
            api_key = vn.get_api_key('namansudans@gmail.com')
            # Note: After getting the OTP, you'll need to enter it in the CLI
        return api_key
    except Exception as e:
        logger.error(f"Error setting up Vanna API: {e}")
        raise
