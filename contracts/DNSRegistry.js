import DNSRegistry from './DNSRegistry.json';

const getContract = async (web3) => {
  const networkId = await web3.eth.net.getId();
  const deployedNetwork = DNSRegistry.networks[networkId];
  return new web3.eth.Contract(
    DNSRegistry.abi,
    deployedNetwork && deployedNetwork.address,
  );
};

export default getContract;