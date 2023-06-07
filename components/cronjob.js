require('dotenv').config();
const k8s = require('@kubernetes/client-node');

async function execCommand() {
  const kc = new k8s.KubeConfig();
  const kubeconfig = `
  apiVersion: v1
  clusters:
  - cluster:
      certificate-authority-data: ${process.env.CERTIFICATE_AUTHORITY}
      server: ${process.env.CLUSTER_SERVER}
    name: ${process.env.CLUSTER_NAME}
  contexts:
  - context:
      cluster: ${process.env.CLUSTER_NAME}
      namespace: ${process.env.NAMESPACE_NAME}
      user: ${process.env.USER_NAME}
    name: ${process.env.CONTEXT_NAME}
  current-context: ${process.env.CONTEXT_NAME}
  kind: Config
  preferences: {}
  users:
  - name: ${process.env.USER_NAME}
    user:
      client-certificate-data: ${process.env.USER_CLIENT_CERTIFICATE}
      client-key-data: ${process.env.USER_CLIENT_KEY} 
  `
  
  kc.loadFromString(kubeconfig);
  //kc.loadFromDefault();

  const namespace = process.env.POD_NAMESPACE;
  const podName = process.env.POD_NAME;
  
  const containerName = process.env.CONTAINER_NAME; 
  const command = ['php73', '/usr/share/ocsinventory-reports/ocsreports/require/components/cron_mailer.php'];    
  
  const exec = new k8s.Exec(kc);
  
  exec.exec(
    namespace,
    podName,
    containerName,
    command,
    process.stdout,
    process.stderr,
    process.stdin
  )
  .then(() => {
    console.log('Comando executado com sucesso!');
  })
  .catch((err) => {
    console.error('Erro ao executar o comando:', err);
  });
}

execCommand();
