from abc import ABCMeta, abstractmethod


class _BGStep:
    """
        A single step in the pipeline
    """
    __metaclass__ = ABCMeta
    param_names = []
    pipe_id = 'id' #overriden by pipeline 

    def __init__(self, params):
        for param_name in self.param_names:
            if not param_name in params:
                raise KeyError('{}: parameter {} is not found in given parameters'.format(
                    self.__class__.__name__, param_name))
        self.params = params
        if not self.validate_params():
            raise ValueError('{}: at least one of the parameters is not valid'.format(
                self.__class__.__name__))

    @abstractmethod
    def run_bg(self, in_dir=None):
        """
        Args
            in_dir: input directory to process
        """
        pass

    @abstractmethod
    def finalize(self, in_dir=None):
        """
        Args
            in_dir: input directory to process
        """
        pass

    def validate_params(self):
        """
            Validates self.params
        """
        return True

    def get_out_dir(self, in_dir):
        """
            in_dir: input directory path
        """
        return in_dir
