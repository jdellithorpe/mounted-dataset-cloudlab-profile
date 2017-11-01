"""This profile sets up a single node with a mounted CloudLab dataset. Useful
for poking around or editing an existing dataset.

Instructions:
Dataset is mounted at /mnt/dataset
"""

# Import the Portal object.
import geni.portal as portal
# Import the ProtoGENI library.
import geni.rspec.pg as pg

import geni.urn as urn
import geni.aggregate.cloudlab as cloudlab

# Create a portal context.
pc = portal.Context()

# Create a Request object to start building the RSpec.
request = pc.makeRequestRSpec()

hardware_types = [ ("m510", "m510 (CloudLab Utah, Intel Xeon-D)"),
                   ("m400", "m400 (CloudLab Utah, 64-bit ARM)"),
                   ("c220g2", "c220g2 (CloudLab Wisconsin, Two Intel E5-2660 v3)") ]

images = [ ("UBUNTU14-64-STD", "Ubuntu 14.04"),
           ("UBUNTU15-04-64-STD", "Ubuntu 15.04"),
           ("UBUNTU16-64-STD", "Ubuntu 16.04")]

pc.defineParameter("hardware_type", "Hardware Type",
                   portal.ParameterType.NODETYPE, 
                   hardware_types[0], hardware_types)

pc.defineParameter("image", "Disk Image",
        portal.ParameterType.IMAGE, images[0], images)

pc.defineParameter("dataset_urn", "URN for Dataset Storage",
    portal.ParameterType.STRING, "")

params = pc.bindParameters()

# Setup a LAN just for the dataset blockstore
datasetbslan = request.LAN()
datasetbslan.best_effort = True
datasetbslan.vlan_tagging = True
datasetbslan.link_multiplexing = True

node = request.RawPC("master")
node.hardware_type = params.hardware_type
if node.hardware_type == "c220g2":
  node.disk_image = urn.Image(cloudlab.Wisconsin,"emulab-ops:%s" % params.image)
else:
  node.disk_image = urn.Image(cloudlab.Utah,"emulab-ops:%s" % params.image)

datasetbs = request.RemoteBlockstore("datasetbs", "/mnt/dataset", "if1")
datasetbs.dataset = params.dataset_urn
datasetbslan.addInterface(datasetbs.interface)
datasetbsiface = node.addInterface("if2")
datasetbslan.addInterface(datasetbsiface)

# Print the RSpec to the enclosing page.
pc.printRequestRSpec(request)
