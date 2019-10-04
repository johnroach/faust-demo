# faustdemo: A simple Helm chart

Run a single pod of faustdemo.

The `templates/` directory contains a very simple pod resource with a
couple of parameters.

The `values.yaml` file contains the default values for the
`faustdemo-pod.yaml` template.

You can install this example using `helm install docs/examples/faustdemo`.
