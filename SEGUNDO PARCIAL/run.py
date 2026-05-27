import importlib.util
import os
import sys


def load_app_package():
    root = os.path.dirname(__file__)
    package_path = os.path.join(root, "app")
    init_path = os.path.join(package_path, "__init__.py")
    spec = importlib.util.spec_from_file_location(
        "app",
        init_path,
        submodule_search_locations=[package_path],
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules["app"] = module
    spec.loader.exec_module(module)
    return module


app_package = load_app_package()
app = app_package.create_app()

if __name__ == "__main__":
    app.run(debug=True)
