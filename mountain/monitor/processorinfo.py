from mountain.core.signals import message_available
from mountain.core.utils import MessageType
from mountain.monitor.models import ProcessorInfo


def handle_proc_info(sender, computer, request_data, msg_data, **kwargs):
    ProcessorInfo.objects.filter(computer=computer).delete()
    for p in msg_data['processors']:
        p_info = ProcessorInfo(computer=computer,
                               processor_id=p['processor-id'],
                               model=p['model'])
        for i in ['cache-size', 'vendor']:
            if p.get(i):
                setattr(p_info, i.replace('-', '_'), p.get(i))

        p_info.save()

    return []


message_available.connect(handle_proc_info,
    sender=MessageType('processor-info'))
