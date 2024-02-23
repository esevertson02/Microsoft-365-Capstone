class Microsoft365Plan:
    def __init__(self,name,  microsoft_email, microsoft_calendar, microsoft_stream, secure_cloud_storage, external_teams_functions, outlook_for_web, web_and_apps, desktop_apps, ai_grammar, copilot, microsoft_loop, lists, forms, schedule_share, video_editing, webinar_functions, compliance, advanced_security, device_management, price_per_user_month):
        self.name = name
        self.microsoft_email = microsoft_email
        self.microsoft_calendar = microsoft_calendar
        self.microsoft_stream = microsoft_stream
        self.secure_cloud_storage = secure_cloud_storage
        self.external_teams_functions = external_teams_functions
        self.outlook_for_web = outlook_for_web #outlook web interface
        self.web_and_apps = web_and_apps
        self.desktop_apps = desktop_apps #Desktop versions of powerpoint, excel, and outlook
        self.ai_grammar = ai_grammar
        self.copilot = copilot
        self.microsoft_loop = microsoft_loop #collaborative workspaces w/ loop
        self.lists = lists #lists app
        self.forms = forms #forms app
        self.schedule_share = schedule_share
        self.video_editing = video_editing #clipchamp
        self.webinar_functions = webinar_functions #webinar functions
        self.compliance = compliance #discover, classify, for auditing and compliance using intune
        self.advanced_security = advanced_security #advanced IAM, protection, 
        self.device_management = device_management #Endpoint device management
        self.price_per_month = price_per_user_month

class BusinessBasic(Microsoft365Plan):
    def __init__(self):
        super().__init__("Business Basic", True, True, True, True, True, True, True, False, False, False, False, True, True, True, False, False, False, False, False, 6.00)

class BusinessStandard(Microsoft365Plan):
    def __init__(self):
        super().__init__("Business Standard", True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, False, False, False, 12.50)


class BusinessPremium(Microsoft365Plan):
    def __init__(self):
        super().__init__("Business Premium", True, True, True, True, True, True, True, True, True, True, True, True, True, True, False, False, True, True, True, 22.00)

class AppsforBusiness(Microsoft365Plan):
    def __init__(self):
        super().__init__("Apps for Business", False, False, False, False, False, False, False, True, False, False, False, False, True, True, False, False, False, False, False, 8.25)