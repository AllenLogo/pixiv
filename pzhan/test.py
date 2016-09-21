from utils import FileUtils

basePath = FileUtils.joinPath(FileUtils.createbasePath(__file__), "/../conf")
print(basePath)