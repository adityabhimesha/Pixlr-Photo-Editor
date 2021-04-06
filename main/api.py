from main.models import Directory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .forms import ImageForm
from django.http import JsonResponse
from django.contrib import messages


# class DirAPI()

class DirectoryAPI(APIView):

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    #Upload Images############
    def post(self, request ,dir, format=None):

        if(request.POST.get('directory_name') == "home"):
            return JsonResponse("Image Cannot Be Named As Home", safe=False)

        try:
            parent_dir = Directory.objects.get(pk=dir)
            if(parent_dir.user_id_id != request.user.id):
                return JsonResponse("You Don't Have Permissions to that DIR", safe=False) 
        except Directory.DoesNotExist:
            parent_dir = None

        if parent_dir is None:
            return JsonResponse("Parent DIR Does Not Exist", safe=False)
        if parent_dir.is_directory == 0:
            return JsonResponse("Parent DIR Cannot Be A File", safe=False)

        form = ImageForm(request.POST, request.FILES)

        if (form.is_valid()):
            form = form.save(commit=False)
            form.user_id_id = request.user.id
            form.parent_directory = parent_dir
            form.is_directory = 0
            form.save()
            payload = "1"
        else:
            return JsonResponse("File Is Not Valid", safe=False)
        return JsonResponse("Image Uploaded Successfully", safe=False)
    

    #Create Folders#############
    def put(self, request, dir, format=None):
 
        if(request.data['name'] == "home"):
            return JsonResponse("Cannot Be Named As Home", safe=False)
        try:
            parent_dir = Directory.objects.get(pk=dir)
            if(parent_dir.user_id_id != request.user.id):
                return JsonResponse("You Don't Have Permissions to that DIR", safe=False) 
        except Directory.DoesNotExist:
            parent_dir = None

        if parent_dir is None:
            return JsonResponse("Parent DIR Does Not Exist", safe=False)
        if parent_dir.is_directory == 0:
            return JsonResponse("Parent DIR Cannot Be A File", safe=False)
    
        new_dir = Directory(user_id=request.user, directory_name=request.data['name'])
        try:
            new_dir.parent_directory = parent_dir
            new_dir.save()
        except:
            return JsonResponse("There Was A Problem!", safe=False)

        return JsonResponse("Folder Created Sucessfully", safe=False)
            

    def delete(self, request, dir, format=None):
        try:
            delete_dir = Directory.objects.get(pk=dir)
            if(delete_dir.user_id_id != request.user.id):
                return JsonResponse("You Don't Have Permissions to that DIR", safe=False) 
        except Directory.DoesNotExist:
            delete_dir = None

        if delete_dir is None:
            return JsonResponse("Parent DIR Does Not Exist", safe=False) 
        if delete_dir.directory_name == "home":
            return JsonResponse("Cannot Delete Home DIR", safe=False) 

        if delete_dir.is_directory == False:
            delete_dir.delete()
        else:
            nodes_to_delete = get_all_child_nodes(delete_dir.id)
            for node in nodes_to_delete:
                Directory.objects.get(pk=node).delete()
                
        return JsonResponse("Folder Deleted Successfully", safe=False)



#BFS traversal for getting all nodes to delete
def get_all_child_nodes(node):
    visited = []   # List to keep track of nodes to be deleted!!.
    queue = []     #Initialize a queue
    visited.append(node)
    queue.append(node)

    while queue:
        s = queue.pop(0)

        for neighbour in Directory.objects.filter(parent_directory=s):
            if neighbour.pk not in visited:
                visited.append(neighbour.pk)
                queue.append(neighbour.pk)
                node = neighbour.pk

    visited.reverse()
    return visited
