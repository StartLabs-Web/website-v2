from mit_moira import Moira

# Initialize Moira client with X.509 certificate and private key file
moira = Moira("./key.pem", "./key.pem")
moira.print_capabilities()
list_name = "startlabs-testing"
username = "chrix"
print(moira.list_members(list_name))
moira.add_member_to_list(list_name, username)


print(moira.user_lists(username))
