class UnsupportedFeature(Exception):
    """
    Custom exception for an unimplemented feature
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
