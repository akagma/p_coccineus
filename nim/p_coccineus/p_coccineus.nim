import std / [
  envvars,
  options,
  os,
  osproc,
]


const blenderVersions = ["4.0", "3.0"]


proc getBlenderExePath(): Option[string] =
  if defined(windows):
    for version in blenderVersions:
      let path = "C:\\Program Files\\Blender Foundation\\Blender " & version & "\\blender.exe"
      if fileExists(path):
        return some(path)
    none(string)
  else:
    none(string)


when isMainModule:
  let currentPythonPath = getEnv("PYTHONPATH")

  let blenderPath = getBlenderExePath()
  if blenderPath.isNone():
    echo "Blender not found."
    quit(1)

  let projectPythonPath =
    if defined(windows):
      getAppDir() & "\\venv\\Lib\\site-packages;" & getAppDir() & "\\python"
    else:
      getAppDir() & "/venv/lib/python3.10/site-packages;" & getAppDir() & "/python"

  if currentPythonPath == "":
    putEnv("PYTHONPATH", projectPythonPath)
  else:
    if defined(windows):
      putEnv("PYTHONPATH", currentPythonPath & ";" & projectPythonPath)
    else:
      putEnv("PYTHONPATH", currentPythonPath & ":" & projectPythonPath)

  echo "PYTHONPATH: " & getEnv("PYTHONPATH")
  echo "Blender exe path: " & blenderPath.get()

  let returnCode = execCmd(blenderPath.get())
  echo "Return code: " & $returnCode
  quit(returnCode)
