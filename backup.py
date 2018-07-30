import pathlib
import subprocess
import gitlab

class BackUp:
   
    def __init__(self, url="https://gitlab.com", private_token="REPLACE", path=".", group="REPLACE"):       
        self.gl = gitlab.Gitlab(url, private_token=private_token)
        self.gl.auth()
        
        self.backup(self.gl.groups.get(group), pathlib.Path(path))
        
    def backup(self, gr, path):
        g_path = path / gr.name
        g_path.mkdir(parents=True, exist_ok=True)

        if hasattr(gr,"projects"):
            for project in gr.projects.list(all=True):
                self._get_project(project, g_path)

        if hasattr(gr,"subgroups"):
            for group in gr.subgroups.list(all=True):
                g_obj = self.gl.groups.get(group.id)
                self.backup(g_obj, path=g_path)

   
    def _get_project(self, project, path):
        p_path = path / project.name
        p_path.mkdir(exist_ok=True)
        
        ssh_url = project.ssh_url_to_repo
    
        subprocess.run(["git", "clone", ssh_url, p_path.as_posix()])
              
if __name__=="__main__":
    a = BackUp()

