from mountain.core.signals import message_available
from mountain.core.utils import MessageType
from mountain.monitor.models import ComputerInfo


def handle_computer_info(sender, computer, request_data, msg_data, **kwargs):
    comp_info, created = ComputerInfo.objects.get_or_create(computer=computer)
    for i in ['total-memory', 'total-swap', 'hostname']:
        setattr(comp_info, i.replace('-', '_'), msg_data[i])
    computer.hostname = msg_data['hostname']
    comp_info.save()
    return []


def handle_distribution_info(sender, computer, request_data, msg_data, **kwargs):
    dist_info, created = ComputerInfo.objects.get_or_create(computer=computer)
    for i in ['code-name', 'description', 'distributor-id', 'release']:
        setattr(dist_info, i.replace('-', '_'), msg_data[i])
    dist_info.save()
    return []


message_available.connect(handle_computer_info,
    sender=MessageType('computer-info'))
message_available.connect(handle_distribution_info,
    sender=MessageType('distribution-info'))
