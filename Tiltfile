# -*- mode: Python -*-

k8s_resource_assembly_version(2)

# kafka-zookeeper
add_repo_script = "git clone https://github.com/confluentinc/cp-helm-charts.git deployment/cp-helm-charts | true"
install_helm_chart = "helm upgrade --install --namespace johnstest -f deployment/kafka-values.yaml confluent deployment/cp-helm-charts"
local(add_repo_script + " && " + install_helm_chart)

# faustdemo worker
k8s_yaml(local('helm template --namespace johntest -f ./deployment/faustdemo-values.yml ./deployment/faustdemo'))
# will need to change this to a remote repo later on
faustdemo_img_name = 'faustdemo'
docker_build(faustdemo_img_name, '.', dockerfile='Dockerfile',
  live_update=[
    sync('.', '/faustdemo'),
    restart_container(),
  ]
)

k8s_resource('release-name-faustdemo', port_forwards=8088)