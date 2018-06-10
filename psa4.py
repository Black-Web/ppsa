# coding = utf-8
class node():
    def __init__(self, index, voltage, load, receive_from, send_through):
        self.index = index
        self.receive_from = receive_from
        self.send_through = send_through
        self.send_through_for_iter = self.send_through.copy()
        self.load = load
        self.voltage = voltage
        self.received_power = load
    def update_power_flow(self):
        self.received_power = self.load\
            +sum([each.transfer_power for each in self.send_through])
    def reset(self):
        self.send_through_for_iter = self.send_through.copy()
    def update_voltage(self,net , current_edge):
        self.voltage = abs(net[current_edge.source_node_index-1].voltage\
                       - current_edge.voltage_loss)

class edge():
    def __init__(self, impedance, connect_to):
        self.impedance = impedance
        self.source_node_index = connect_to[0]
        self.user_node_index = connect_to[1]
        # self.modified = False
        self.power_loss = 0
        self.voltage_loss = 0
        self.transfer_power = 0
    def update_power_flow(self, net):
        send_power = net[self.user_node_index-1].received_power
        voltage = net[self.user_node_index-1].voltage
        self.power_loss = self.impedance * abs(send_power/voltage)**2
        self.transfer_power = self.power_loss + send_power
        # self.modified = True
    def update_voltage(self, voltage):
        self.voltage_loss = self.transfer_power\
             * self.impedance.conjugate() / voltage

edge1 = edge(1+1j,[1,2])
edge2 = edge(1+2j,[2,3])
edge3 = edge(2+2j,[2,4])
edge4 = edge(2+1j,[4,5])
edges = [edge1,edge2,edge3,edge4]

node1 = node(1,10,0.2+0.2j, None , {edge1})
node2 = node(2,10,0.2+0.2j, edge1, {edge2,edge3})
node3 = node(3,10,0.4+0.4j, edge2, set())
node4 = node(4,10,0.4+0.4j, edge3, {edge4})
node5 = node(5,10,0.4+0.4j, edge4, set())
nodes = [node1,node2,node3,node4,node5]
leaf_node = [each for each in nodes if not each.send_through]

def update_voltage(source_node,current_edge,current_node):
    current_edge.update_voltage(source_node.voltage)
    current_node.update_voltage(nodes, current_edge)
    # if current_node.send_through_for_iter: 
    for current_edge in current_node.send_through_for_iter:
        source_node = current_node
        # current_edge = source_node.send_through_for_iter.pop()
        current_node = nodes[current_edge.user_node_index-1]
        update_voltage(source_node,current_edge,current_node)

V = [each.voltage for each in nodes]
S = [each.transfer_power for each in edges]
while True:
    nodeiter = leaf_node.copy()
    current_node = nodeiter.pop()
    while True:
        current_edge = current_node.receive_from
        source_node = nodes[current_edge.source_node_index-1]
        current_edge.update_power_flow(nodes)
        source_node.update_power_flow()
        source_node.send_through_for_iter.remove(current_edge)
        if source_node.send_through_for_iter:
            try:current_node = nodeiter.pop()
            except:print('unexpected iteration error.')
        elif source_node.receive_from:
            current_node = source_node
        else:
            for each in nodes:
                each.reset()
            break
    update_voltage(source_node,current_edge,current_node)
    if max([abs(vn - vn_1) for vn,vn_1 in\
            zip([each.voltage for each in nodes], V)])>1e-6:
        V = [each.voltage for each in nodes]
        S = [each.transfer_power for each in edges]
    else:break

print('每个节点电压：\n',V)
print('每条支路功率：\n',S)