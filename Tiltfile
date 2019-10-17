# -*- mode: Python -*-

k8s_resource_assembly_version(2)

# user-namespace creator
namespace_yaml = helm(
  paths='deployment/tilt-namespace',
  name='testspace-namespace',
  namespace='default',
  values=['./deployment/namespace-values.yml'])
k8s_yaml(namespace_yaml)

# Confluent kafka-zookeeper
add_repo_script = "git clone https://github.com/confluentinc/cp-helm-charts.git deployment/cp-helm-charts | true"
local(add_repo_script)
confluent_yaml = helm(
  paths='deployment/cp-helm-charts',
  name='confluent',
  namespace='testspace',
  values=['./deployment/kafka-values.yml'])
k8s_yaml(confluent_yaml)
k8s_resource('confluent-cp-control-center',port_forwards=9021)


# faustdemo worker
k8s_yaml(local('helm template --namespace johntest -f ./deployment/faustdemo-values.yml ./deployment/faustdemo'))
# will need to change this to a remote repo later on
faustdemo_img_name = 'faustdemo'
docker_build(faustdemo_img_name, '.', dockerfile='Dockerfile',
  live_update=[
    sync('faustdemo', '/faustdemo/faustdemo'),
    run('rm -rf faustdemo/page_views/__pycache__'),
    run('find . | grep py | grep page_views'),
    restart_container(),
  ]
)
k8s_resource('release-name-faustdemo', port_forwards=8088)