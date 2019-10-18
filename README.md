# Faust demo project

This project is a demo of what can be done via the Faust framework which is a stream processing library, porting the ideas from [Kafka Streams](https://kafka.apache.org/documentation/streams/) to Python. Faust provides both stream processing and event processing.

## Summary of demo

The demo has 3 pages:

- [`/`](http://localhost:8088/): A basic health check
- [`/ready/`](http://localhost:8088/ready/): States when the worker is actually ready and recovery is complete.
- [`/count/`](http://localhost:8088/count/): Increases count in memory on page laod and sends result into `page_views_topic`. The agent `aggregate_page_views` will pick up events and add it to a tumbling windowed table `tumbling_page_view_table`. Please check the following documentation to learn about agents, windows and tables here:
  - [**Tables and Windowing**](https://faust.readthedocs.io/en/latest/userguide/tables.html#tables-and-windowing)
  - [**Agents - Self-organizing Stream Processors**](https://faust.readthedocs.io/en/latest/userguide/agents.html)
- [`/report/`](http://localhost:8088/report/): Will show the present values in table. Not to be relied on in production environments.

First run might take some time due to RocksDB installation. RocksDB is very useful when dealing with failures when processing streaming data in a tabled fashion.

### Requirements

- [Python 3.7+](https://www.python.org/downloads/)
- [Poetry](https://poetry.eustace.io/docs/#installation)
- [Docker](https://docs.docker.com/docker-for-mac/install/)

**If** you would want to use **Tilt** you might want to install:

- [helm](https://helm.sh/docs/using_helm/#installing-the-helm-client)
- [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
- [kubectx](https://github.com/ahmetb/kubectx#macos)
- [docker-kubernetes](https://docs.docker.com/docker-for-mac/#kubernetes)

**You don't have to use Tilt!** docker-compose is also available.

You can learn more about [Tilt here](http://tilt.dev). In summary allows you to use Kubernetes which allows you to capture possible edge cases and gotchas in regards to streaming processing in your development environment.

### Running the demo

If using docker-compose:

```bash
make run-dev
```

If using Tilt:

```bash
make run-dev-tilt
```

If you want to run natively(you will need to set Kafka up yourself or use docker-compose):

```bash
make native-run
```

#### Debugging issues in running demo

When running natively you might get a failure in regards to clang. Well, you will need to install clang. This usually should come with xcode. Simply run xcode and install needed packages:

![https://zappy.zapier.com/33F1A566-7635-4161-9E65-B4A64F865E40.png](https://zappy.zapier.com/33F1A566-7635-4161-9E65-B4A64F865E40.png)

If you still have the same issue. It might be you are using the wrong MacOSX.sdk.

Check `/Library/Developer/CommandLineTools/SDKs` and make sure `MacOSX.sdk` points to latest and any python library getting built uses latest version of SDK for builds.

### Running Tests

Simply run:

```bash
make test
```
## Deployment

### Deployment Topology and Behavior

In production deployments the management of a cluster of worker instances is complicated by the Kafka rebalancing strategy.

Every time a new worker instance joins or leaves, the Kafka broker will ask all instances to perform a “rebalance” of available partitions.

This “stop the world” process will temporarily halt processing of all streams, and if this rebalancing operation is not managed properly, you may end up in a state of perpetual rebalancing: the workers will continually trigger rebalances to occur, effectively halting processing of the stream.

> The Faust web server is not affected by rebalancing, and will still serve web requests.
> This is important to consider when using tables and serving table data over HTTP. Tables exposed in this manner will be eventually consistent and may serve stale data during a rebalancing operation.

When will rebalancing occur? It will occur should you restart one of the workers, or when restarting workers to deploy changes, and also if you change the number of partitions for a topic to scale a cluster up or down.

To restart the worker you should send the `TERM` signal and start a new instance. Shutdown is accomplished using the `TERM` signal.

The worker's main process overrides the following signals:

| Signal   |      Effect      |
|----------|:-------------:|
| `TERM` |  Warm shutdown, wait for tasks to complete. |
| `QUIT` |    Cold shutdown, terminate ASAP   |
| `USR1` | Dump traceback for all active threads in logs |

### Restarting a cluster

To minimize the chance of rebalancing problems we suggest you use the following strategy to restart all the workers:

1. Stop 50% of the workers (and wait for them to shut down).
2. Start the workers you just stopped and wait for them to fully start.
3. Stop the other half of the workers (and wait for them to shut down).
4. Start the other half of the workers.

You should also think of adjusting rebalancing configurations and give a delay to this action.

This should both minimize rebalancing issues and also keep the built-in web servers up and available to serve HTTP requests.

## TODO

- [ ] Create CI/CD pipeline
- [ ] Move into project template or make it a project template
- [ ] Tie in schema registry for data models
- [ ] Add statsd and/or datadog implementation
- [ ] Add livecheck for production
- [ ] Add examples for Tasks and Timers