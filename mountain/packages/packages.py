from mountain.core.signals import message_available
from mountain.core.utils import MessageType
from mountain.packages.models import PackageHash
from mountain.packages.utils import get_hash

def handle_unknown_hashes(sender, computer, request_data, msg_data, **kwargs):
    hashes = [i.encode('hex') for i in msg_data['hashes']]
    data = PackageHash.objects.hashes_in_bulk(hashes)
    ids = [(data.get(hash).id if data.get(hash) else None) for hash in hashes]
    return [{'type': 'package-ids', 'ids':ids, 'request-id':msg_data['request-id']}]

def handle_add_packages(sender, computer, request_data, msg_data, **kwargs):
    ids = []
    for p in msg_data['packages']:
        hash = get_hash(p['type'], p['name'], p['version'], p['relations'])
        m = PackageHash(hash = hash)
        for i in ('name', 'summary', 'version', 'description',
            'installed-size', 'size', 'type', 'section'):
            setattr(m, i.replace('-', '_'), p.get(i))
        # TODO: that's ugly
        try:
            m.save()
            ids.append(m.id)
        except Exception, e:
            print p
            print e

    return [{'type': 'package-ids', 'ids':ids, 'request-id':msg_data['request-id']}]

message_available.connect(handle_unknown_hashes, sender=MessageType("unknown-package-hashes"))
message_available.connect(handle_add_packages, sender=MessageType("add-packages"))
