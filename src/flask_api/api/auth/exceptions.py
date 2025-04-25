from werkzug.exceptions import Unauthorized, Forbidden

_REALM_REGULAR_USERS = "registered_users@mydomain.com"
_REALM_ADMIN_USERS = "admin_users@mydomain.com"

class ApiUnauthorized(Unauthorized):
    """Exception raised for unauthorized access."""

    def __init__(
        self, 
        description="Unauthorized", 
        admin_only=False, 
        error=None, 
        error_description=None,
        content_type="application/json"
    ):
        
        self.description = description
        www_auth_value = self.__get_www_auth_value(
            admin_only, error, error_description
        )
        
        super().__init__(
            self, description=description, response=None, www_authenticate=www_auth_value
        )
    
    def get_headers(self, environ):
        """Override the get_headers method to include WWW-Authenticate header.
        :return: List of headers including WWW-Authenticate and Content-Type.
        """
        
        headers = super().get_headers(environ)
        headers = [(name, value) for name, value in headers if name != "content-type"]
        headers.append(("Content-Type", self.content_type))
        return headers
    
    
    def __get_www_auth_value(self, admin_only, error, error_description):
        realm = _REALM_ADMIN_USERS if admin_only else _REALM_REGULAR_USERS
        parts = [f'Bearer realm="{realm}"']
        if error:
            parts.append(f'error="{error}"')
        if error_description:
            parts.append(f'error_description="{error_description}"')
        return ", ".join(parts)  
    
    
class ApiForbidden(Forbidden):
    """Exception raised for forbidden access."""

    description = "You Are Not Allowed To Access This Resource"
    
    def __init__(content_type: str = "application/json"):
        self.content_type = content_type
        
    
    def get_headers(self, environ):
        return [
            ("Content-Type", content_type),
            
            (
                "WWW-Authenticate",
                f'Bearer realm="{_REALM_ADMIN_USERS}", '
                'error="insufficient_scope", '
                'error_description="You are not an administrator"',
            ),
        ]