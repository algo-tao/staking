script = '/root/workspace/staking/neurons/miner.py'
uvicorn = '/root/workspace/staking/.venv/bin/uvicorn'
interpreter = '/root/workspace/staking/.venv/bin/python'
PYTHONPATH = '/root/workspace/staking:$PYTHONPATH'
TZ = 'UTC'
TAOCD_LOGER_PATH = '/root/workspace/staking/logs'
TAOCD_PWD = '/root/workspace/staking'
HOST_IP = '38.126.208.155'
EXTERNAL_IP = '38.126.208.155'

const appConfig = Array.from({length:1}).reduce((pre,cur,index)=>{
  const coldGroup = Array.from({length:10}).map((v,i)=>{
    const cdNum = index+1
    const zeroNum = String(i + 1).padStart(2, '0')
    const port = i < 20 ? (9500 + index * 20 + i + 1) : (9600 + index * 20 + i + 1 - 20)
    const taocdName = `taocd88_0${cdNum}.taocd${cdNum}_${zeroNum}`
    const coldkey = `taocd88_0${cdNum}`
    const hotkey = `taocd${cdNum}_${zeroNum}`
    const external_ip = EXTERNAL_IP
    return {
      name: taocdName,
      script: script,
      args: `--wallet.name ${coldkey} --wallet.hotkey ${hotkey} --subtensor.network finney --netuid 88 --subtensor.chain_endpoint ws://162.244.82.223:9944 --axon.port ${port} --axon.external_ip ${external_ip} --logging.debug --logging.logging_dir ${TAOCD_LOGER_PATH}/${taocdName}`,
      interpreter,
      env: {
          PYTHONPATH,
          TZ,
          TAOCD_LOGER_PATH: `${TAOCD_LOGER_PATH}/${taocdName}`,
          HOST_IP
      },
      out_file: `${TAOCD_LOGER_PATH}/${taocdName}/output.log`,
      error_file: `${TAOCD_LOGER_PATH}/${taocdName}/error.log`,
      restart_delay: 60 * 1000 * 5
    }
  }).filter(v=>v)
  return [...pre,...coldGroup]
},[]).filter(v=>v)

module.exports = {
    apps: [...appConfig]
}