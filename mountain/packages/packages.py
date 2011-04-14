from mountain.core.signals import message_available
from mountain.core.utils import MessageType
from mountain.packages.models import Package, PackageRelation, PackageStatus, STATUS_CHOICES
from mountain.packages.utils import get_hash

def handle_unknown_hashes(sender, computer, request_data, msg_data, **kwargs):
    hashes = [i.encode('hex') for i in msg_data['hashes']]
    data = Package.objects.hashes_in_bulk(hashes)
    ids = [(data.get(hash).id if data.get(hash) else None) for hash in hashes]
    return [{'type': 'package-ids', 'ids':ids, 'request-id':msg_data['request-id']}]

def handle_add_packages(sender, computer, request_data, msg_data, **kwargs):
    ids = []
    for p in msg_data['packages']:
        hash = get_hash(p['type'], p['name'], p['version'], p['relations'])
        m = Package(hash=hash)
        for i in ('name', 'summary', 'version', 'description',
            'installed-size', 'size', 'type', 'section'):
            setattr(m, i.replace('-', '_'), p.get(i))
        m.save()
        for relation in p['relations']:
            PackageRelation.objects.create(package=m, type=relation[0],
                                           target=relation[1])
        ids.append(m.id)

    return [{'type': 'package-ids', 'ids':ids, 'request-id':msg_data['request-id']}]

STATUS_TO_ID = dict(map(lambda x: x[::-1], STATUS_CHOICES))

def handle_packages(sender, computer, request_data, msg_data, **kwargs):
    for status in ('installed', 'available', 'available-upgrades', 'locked'):
        ids = []
        remove_ids = []

        for remove in (False, True):
            s = status if not remove else 'not-%s' % status
            for id_or_range in msg_data.get(s, []):
                ids_ = ids if not remove else remove_ids
                if isinstance(id_or_range, tuple):
                    ids_.extend(range(id_or_range[0], id_or_range[1]+1))
                else:
                    ids_.append(id_or_range)

        for id in ids:
            PackageStatus.objects.create(computer=computer,
                package_id=id, status=STATUS_TO_ID[status])
        if remove_ids:
            PackageStatus.objects.delete(computer=computer,
                package_id__in=remove_ids)

    return []

message_available.connect(handle_unknown_hashes, sender=MessageType('unknown-package-hashes'))
message_available.connect(handle_add_packages, sender=MessageType('add-packages'))
message_available.connect(handle_packages, sender=MessageType('packages'))
