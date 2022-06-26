def packages_installed(packages):
    if isinstance(packages, list):

        import pip
        for package in packages:
            try:
                __import__(package)
            except ImportError:
                pip.main(['install', '--user', package])
                
    else:
        raise ValueError("Function argument \"packages\" must be list")