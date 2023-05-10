import uvicorn
import fastapi
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter
)

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter

from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import  start_http_server
import time
import random

OTLP_HOST=""
SERVICE_NAME="opentelemetry-testing"
provider = TracerProvider(
    resource=Resource.create({SERVICE_NAME:SERVICE_NAME})
)

processor = BatchSpanProcessor(
    # ConsoleSpanExporter(),
    # InMemorySpanExporter(),
    OTLPSpanExporter(endpoint=OTLP_HOST, insecure=True)
)
provider.add_span_processor(processor)
# Sets the global default tracer provider
trace.set_tracer_provider(provider)
# Creates a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)



app = fastapi.FastAPI()


@app.get("/foo")
def foobar():
    time.sleep(random.uniform(0,10))
    current_span = trace.get_current_span()
    span_context = current_span.context
    trace_id = trace.format_trace_id(span_context.trace_id) 
    return {"message": trace_id}

@app.get("/bar")
def bar():
    return {"message": "bar"}

tp = trace.get_tracer_provider()
test = Instrumentator().instrument(app)
FastAPIInstrumentor.instrument_app(app)






if __name__ == "__main__":
    start_http_server(port=5005, registry=test.registry)
    uvicorn.run("main:app", port=5000, host="0.0.0.0",log_level="info", workers=1)