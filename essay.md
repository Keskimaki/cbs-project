LINK: https://github.com/Keskimaki/csb-project Django project so no installation instructions needed.

Injection (XSS): https://github.com/Keskimaki/cbs-project/blob/18876df273028e0602d1a5a102019c7818dca467/src/pages/templates/pages/app.html#L14

Cross-site scripting (XSS) is under injection in OWASP top ten list for 2021. XSS allows the attacker to inject malicious code into the application in such a way as to make the user’s computer run that code. In the case of my project the attacker can send a message to another user that is supposed to only contain text. The input is displayed within a HTML document. The HTML document is written so that the message variable is not inside any tags like `<li>` or `<p>`. Because of this the attacker can for example use `<script>` tag in their message and the browser will interpret the text inside as JavaScript code that is a part of the program and run the code inside.

The fix is to simply use some tag for the message variable in the HTML document. The commented out version of the code does exactly this. It renders the messages inside an unordered list within `<li>` tags. In that case the browser will interpret <script> as a part of the text message and not as JS code that it need to run. Django also automatically escapes HTML preventing any XSS attacks by default. To prevent this the message variable had to be marked as safe.

Cross-site Request Forgery https://github.com/Keskimaki/cbs-project/blob/18876df273028e0602d1a5a102019c7818dca467/src/pages/templates/pages/login.html#L11

With cross-site request forgery (CSRF) the attacker uses an authenticated users credentials to their advantage during the users session. For example if a user is logged into an application and uses a secondary tab for other things. The browser stores the user session of the first website even while using the secondary tab. Without CSRF protection the second website could access the user session and send authenticated post requests to the original site. The request would seem acceptable to the original server since the server does not care which frontend was used to send the requests, but only the data included.

In the case of this Django project the inbuilt CSRF protection can simply be activated by writing `{{% csrf_token %}}` within the HTML form. Most modern frameworks and browsers have inbuilt CSRF protection. Django’s also immediately warns about the vulnerability so it’s unlikely to get to all the way to production unnoticed. Just to get the program running with the vulnerability the inbuilt Django CSRF middleware also had to be disabled.

Cryptographic Failure https://github.com/Keskimaki/cbs-project/blob/18876df273028e0602d1a5a102019c7818dca467/src/pages/models.py#L5 OWASP calls any cryptography related failure leading to sensitive data exposure a cryptographic failure. It is the second most important security risk for web applications. My project contains likely the most elementary form of cryptographic failure namely the complete lack of cryptography. The user passwords are stored as plain text so anyone who gets access to the database has full access to all accounts. The passwords and usernames can then likely be used to break into other accounts of the users.

Django has inbuilt capabilites for password storage as well as support for external packages such as bcrypt. Django documentation https://docs.djangoproject.com/en/4.0/topics/auth/passwords/ seems to contain many different options for solving this problem. Personally I would likely encrypt the passwords using bcrypt since I am familiar with it from earlier projects. The lack of encryption did slightly simplify the project, but made it far less secure.

Insecure Design https://github.com/Keskimaki/cbs-project/blob/18876df273028e0602d1a5a102019c7818dca467/src/pages/views.py#L51

The somewhat generic category of insecure design is the fourth most significant security risk on the OWASP list. In my project insecure design can be seen in all the other vulnerabilities listed here, but especially on the completely unsecured database path. The path is meant to be used by the developer or administrator to visually see all the application’s data. The problem is that anyone who happens to figure out the /db path can access it. The problem becomes very significant because of the earlier cryptographic failure as all the passwords are completely visible in plain text.

Easiest fix would be to delete the entire feature. The data can be seen by through the Django admin portal and with direct SQL commands anyway. Other option would be to at least require password or some other form of authentication when accessing /db.

Security Misconfiguration
No link to the code since the vulnerability appears during Django configuration

OWASP lists security misconfiguration as the fifth most significant security risk. Django includes inbuilt warnings for insecure configuration, but most of these warnings can be skipped, since in the end Django needs to trust the developer to know what they are doing. In my project I configured the project with an admin account as instructed in Django’s starting guide. I configured the account with the name admin and password admin. Django warned about the insecure password, but I skipped the warning and so doing created a security vulnerability. The username and password used are easily guessable by simply trying a couple times and would be broken quickly by using lists of commonly used usernames and passwords.

The problem is very simple to fix. I would only need to listen to Django’s warnings and select a stronger password and perhaps also a less obvious username.
