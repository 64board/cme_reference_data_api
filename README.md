# cme_reference_data_api
CME Reference Data API Version 2

https://www.cmegroup.com/confluence/display/EPICSANDBOX/CME+Reference+Data+API+Version+2

CME Reference Data API version 2 uses OAuth, an open protocol that supports secure authorization in a simple, standard method and decouples authentication from authorization.

A registered OAuth API ID is required to access the CME Reference Data API version 2 services.  API IDs for CME Group Logins are created and managed in the Customer Center under My Profile.

https://login.cmegroup.com/sso/navmenu.action

OAuth 2.0 Authorization Server Endpoints

New Release
https://authnr.cmegroup.com/as/token.oauth2

Production
https://auth.cmegroup.com/as/token.oauth2

Query URLs

New Release
http://api.refdata.nr.cmegroup.com/

Production
http://api.refdata.cmegroup.com/

Authorized API ID's may access three endpoints in the New release and Production environments:

New Release Endpoints:

    /v2/products
    /v2/instruments
    /v2/displayGroups

Production Endpoints:

    /v2/products
    /v2/instruments
    /v2/displayGroups
