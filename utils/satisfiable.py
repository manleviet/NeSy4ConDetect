from flamapy.metamodels.configuration_metamodel.transformations import ConfigurationBasicReader
from flamapy.metamodels.fm_metamodel.transformations import UVLReader
from flamapy.metamodels.pysat_metamodel.operations import PySATSatisfiableConfiguration
from flamapy.metamodels.pysat_metamodel.transformations import FmToPysat

file = "../data/busybox/kb/busybox.uvl"


feature_model = UVLReader(file).transform()
configuration = ConfigurationBasicReader("./resource_satisfiable/invalid_conf_1_1.txt").transform()

sat_model = FmToPysat(feature_model).transform()
satisfiable = PySATSatisfiableConfiguration()
satisfiable.set_configuration(configuration)
result = satisfiable.execute(sat_model)

print(result.result)