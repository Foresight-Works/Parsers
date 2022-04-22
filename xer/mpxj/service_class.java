package com.fsw.bo.service.util;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.jdom2.Document;
import org.jdom2.Element;
import org.jdom2.output.Format;
import org.jdom2.output.XMLOutputter;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;

import com.fsw.bo.util.Constants;
import com.fsw.bo.util.Utils;

import net.sf.mpxj.ActivityStatus;
import net.sf.mpxj.ActivityType;
import net.sf.mpxj.Relation;
import net.sf.mpxj.Task;

@Service
public class GraphMLConverter {

	private static final Logger logger = LogManager.getLogger(GraphMLConverter.class);

	private Map<ActivityType, String> activityType = new HashMap<>();
	private Map<ActivityStatus, String> activityStatus = new HashMap<>();
	private Map<String, String> graphMlTaskColors = new HashMap<>();

	/**
	 *
	 */
	public void initTaskColorMap() {
		graphMlTaskColors.put(Constants.TT_TASK, Constants.GRAPH_ML_COLOR_RED);
		graphMlTaskColors.put(Constants.TT_FIN_MILE, Constants.GRAPH_ML_COLOR_BLUE);
		graphMlTaskColors.put(Constants.TT_LOE, Constants.GRAPH_ML_COLOR_YELLOW);
	}

	/**
	 *
	 */
	private Element initGraphML() {

		Element graphMLElement = new Element(Constants.GRAPH_ML_ELEMENT);
		buildGraphAttributes(graphMLElement);
		initTaskColorMap();
		return graphMLElement;
	}

	/**
	 * @param graphMLElement
	 */
	public void buildGraphAttributes(Element graphMLElement) {

		List<GraphMLAttributes> keys = new ArrayList<GraphMLAttributes>();
		keys.add(new GraphMLAttributes("d0", "color", "string", "node", "black"));
		keys.add(new GraphMLAttributes("d1", "weight", "double", "edge", "1.0"));
		keys.add(new GraphMLAttributes("d2", "color", "string", "edge", "black"));
		keys.add(new GraphMLAttributes("Label", "Label", "string", "node", null));
		keys.add(new GraphMLAttributes("TaskType", "TaskType", "string", "node", null));
		keys.add(new GraphMLAttributes("PlannedStart", "PlannedStart", "string", "node", null));
		keys.add(new GraphMLAttributes("PlannedEnd", "PlannedEnd", "string", "node", null));
		keys.add(new GraphMLAttributes("ActualStart", "ActualStart", "string", "node", null));
		keys.add(new GraphMLAttributes("ActualEnd", "ActualEnd", "string", "node", null));
		keys.add(new GraphMLAttributes("Status", "Status", "string", "node", null));
		keys.add(new GraphMLAttributes("Float", "Float", "integer", "node", null));
		keys.add(new GraphMLAttributes("r", "r", "integer", "node", null));
		keys.add(new GraphMLAttributes("g", "g", "integer", "node", null));
		keys.add(new GraphMLAttributes("b", "b", "integer", "node", null));
		keys.add(new GraphMLAttributes("Constraint", "Constraint", "string", "node", null));
		keys.add(new GraphMLAttributes("ConstraintDate", "ConstraintDate", "string", "node", null));
		keys.add(new GraphMLAttributes("edgelabel", "edgelabel", "string", "edge", null));
		keys.add(new GraphMLAttributes("Dependency", "Dependency", "string", "edge", null));
		keys.add(new GraphMLAttributes("DependencyLag", "DependencyLag", "integer", "edge", null));

		for (GraphMLAttributes attr : keys) {
			Element key = new Element(Constants.KEY_ELEMENT);
			key.setAttribute(Constants.ID_ATTRIBUTE, attr.getId());
			key.setAttribute(Constants.ATTR_NAME_ATTRIBUTE, attr.getName());
			key.setAttribute(Constants.ATTR_TYPE_ATTRIBUTE, attr.getType());
			key.setAttribute(Constants.FOR_ATTRIBUTE, attr.getGraphComponent());

			if (attr.getDefaultVal() != null) {
				Element defaultElement = new Element(Constants.DEFAULT_ELEMENT);
				defaultElement.addContent(attr.getDefaultVal());
				key.addContent(defaultElement);
			}
			graphMLElement.addContent(key);
		}
	}

	/**
	 * @param fileName
	 * @param taskList
	 * @param activityTypeMap
	 * @param activityStatusMap
	 * @return
	 * @throws Exception
	 */
	public Resource convert(List<Task> taskList, Map<ActivityType, String> activityTypeMap,
			Map<ActivityStatus, String> activityStatusMap) throws Exception {

		Resource converted = null;
		activityType.putAll(activityTypeMap);
		activityStatus.putAll(activityStatusMap);
		Element graphMLElement = initGraphML();
		buildGraph(taskList, graphMLElement);

		Document document = new Document(graphMLElement);
		converted = save(document);
		return converted;
	}

	/**
	 * @param tasks
	 * @param graphml
	 * @throws Exception
	 */
	public void buildGraph(List<Task> tasks, Element graphml) throws Exception {

		Element graph = new Element(Constants.GRAPH_ELEMENT);
		graph.setAttribute(Constants.ID_ATTRIBUTE, "Graph");
		graph.setAttribute(Constants.EDGE_DEFAULT_ATTRIBUTE, "directed");
		graphml.addContent(graph);
		
		List<Task> taskList = tasks.stream().filter(e -> e.getActivityType() != null)
				.filter(e -> !ActivityType.LEVEL_OF_EFFORT.name().equals(e.getActivityType().name())).collect(Collectors.toList());

		buildGraphNodes(taskList, graph);
		buildGraphEdges(taskList, graph);
	}

	/**
	 * @param tasks
	 * @param graph
	 * @throws Exception
	 */
	private void buildGraphNodes(List<Task> tasks, Element graph) throws Exception {

		for (Task task : tasks) {
			
			Element node = new Element(Constants.NODE_ELEMENT);
			node.setAttribute(Constants.ID_ATTRIBUTE, task.getActivityID());

			Element d0 = new Element(Constants.DATA_ELEMENT);
			d0.setAttribute(Constants.KEY_ATTRIBUTE, "d0");
			d0.setText(getGraphMLTaskColor(task));
			node.addContent(d0);

			Element label = new Element(Constants.DATA_ELEMENT);
			label.setAttribute(Constants.KEY_ATTRIBUTE, "Label");
			label.setText(task.getName());
			node.addContent(label);

			Element taskType = new Element(Constants.DATA_ELEMENT);
			taskType.setAttribute(Constants.KEY_ATTRIBUTE, "TaskType");
			taskType.setText(activityType.get(task.getActivityType()));
			node.addContent(taskType);

			if (task.getPlannedStart() != null) {
				Element plannedStart = new Element(Constants.DATA_ELEMENT);
				plannedStart.setAttribute(Constants.KEY_ATTRIBUTE, "PlannedStart");
				plannedStart.setText(Utils.ddMMyyyy.format(task.getPlannedStart()));
				node.addContent(plannedStart);
			}

			if (task.getPlannedFinish() != null) {
				Element plannedEnd = new Element(Constants.DATA_ELEMENT);
				plannedEnd.setAttribute(Constants.KEY_ATTRIBUTE, "PlannedEnd");
				plannedEnd.setText(Utils.ddMMyyyy.format(task.getPlannedFinish()));
				node.addContent(plannedEnd);
			}

			if (task.getActualStart() != null) {
				Element actualStart = new Element(Constants.DATA_ELEMENT);
				actualStart.setAttribute(Constants.KEY_ATTRIBUTE, "ActualStart");
				actualStart.setText(Utils.ddMMyyyy.format(task.getActualStart()));
				node.addContent(actualStart);
			}

			if (task.getActualFinish() != null) {
				Element actualEnd = new Element(Constants.DATA_ELEMENT);
				actualEnd.setAttribute(Constants.KEY_ATTRIBUTE, "ActualEnd");
				actualEnd.setText(Utils.ddMMyyyy.format(task.getActualFinish()));
				node.addContent(actualEnd);
			}

			if (task.getFreeSlack() != null) {
				Element freeFloat = new Element(Constants.DATA_ELEMENT);
				freeFloat.setAttribute(Constants.KEY_ATTRIBUTE, "Float");
				Double duration = task.getFreeSlack().getDuration();
				freeFloat.setText(String.valueOf(duration.intValue()));
				node.addContent(freeFloat);
			}

			Element status = new Element(Constants.DATA_ELEMENT);
			status.setAttribute(Constants.KEY_ATTRIBUTE, "Status");
			status.setText(activityStatus.get(task.getActivityStatus()));
			node.addContent(status);

			if (task.getConstraintDate() != null) {
				Element constraint = new Element(Constants.DATA_ELEMENT);
				constraint.setAttribute(Constants.KEY_ATTRIBUTE, "Constraint");
				constraint.setText(task.getConstraintType().name());
				node.addContent(constraint);

				Element constraintDate = new Element(Constants.DATA_ELEMENT);
				constraintDate.setAttribute(Constants.KEY_ATTRIBUTE, "ConstraintDate");
				constraintDate.setText(Utils.ddMMyyyy.format(task.getConstraintDate()));
				node.addContent(constraintDate);
			}
			graph.addContent(node);
		}
	}

	/**
	 * @param tasks
	 * @param graph
	 */
	private void buildGraphEdges(List<Task> tasks, Element graph) {

		for (Task task : tasks) {
			List<Relation> successors = task.getSuccessors();
			if (successors != null && !successors.isEmpty()) {
				for (Relation relation : successors) {
					if(relation.getTargetTask().getActivityType() != null &&
							!relation.getTargetTask().getActivityType().equals(ActivityType.LEVEL_OF_EFFORT)) {
						String source = relation.getSourceTask().getActivityID();
						String target = relation.getTargetTask().getActivityID();
	
						Element edge = new Element(Constants.EDGE_ELEMENT);
						edge.setAttribute(Constants.ID_ATTRIBUTE, source + "-" + target);
						edge.setAttribute(Constants.SOURCE_ATTRIBUTE, source);
						edge.setAttribute(Constants.TARGET_ATTRIBUTE, target);
	
						Element dependency = new Element(Constants.DATA_ELEMENT);
						dependency.setAttribute(Constants.KEY_ATTRIBUTE, "Dependency");
						dependency.setText(relation.getType().toString());
						edge.addContent(dependency);
	
						Element dependencyLag = new Element(Constants.DATA_ELEMENT);
						dependencyLag.setAttribute(Constants.KEY_ATTRIBUTE, "DependencyLag");
						Double duration = relation.getLag().getDuration();
						dependencyLag.setText(String.valueOf(duration.intValue()));
						edge.addContent(dependencyLag);
						graph.addContent(edge);
					}
				}
			}
		}
	}

	/**
	 * print the content of the document (only for test)
	 *
	 * @param doc xml document
	 */
	public void printAll(Document doc) {
		try {
			XMLOutputter outputter = new XMLOutputter();
			outputter.output(doc, System.out);
		} catch (java.io.IOException e) {
			logger.error("Error:", e);
		}
	}

	/**
	 * write the xml document into file
	 *
	 * @param file the file name
	 * @param doc  xml document
	 * @throws Exception
	 */
	public Resource save(Document doc) throws Exception {

		XMLOutputter outputter = new XMLOutputter(Format.getPrettyFormat());
		String xml = outputter.outputElementContentString(doc.getRootElement());

		/*
		 * Using StringBuilder and not a standard way(XMLOutputter object) to create
		 * graphml file because of xmlns="" needless namespace which is causing grapml
		 * file failure
		 */
		StringBuilder graphMl = new StringBuilder();
		graphMl.append("<?xml version=\"1.0\" encoding=\"UTF-8\"?>").append("\n");
		graphMl.append("<graphml xmlns=\"http://graphml.graphdrawing.org/xmlns\"").append(" ");
		graphMl.append(
				"xmlns:schemLocation=\"http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd\"")
				.append(" ");
		graphMl.append("xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"").append(">").append("\n");
		graphMl.append(xml).append("\n");
		graphMl.append("</graphml>");

		Resource resource = getFileResource(graphMl.toString());
		return resource;
	}

	/**
	 * @param graphMl
	 * @return
	 * @throws IOException
	 */
	public static Resource getFileResource(String graphMl) throws IOException {

		Path tempFile = Files.createTempFile("GraphML_File_", ".graphml");
		Files.write(tempFile, graphMl.getBytes());
		File file = tempFile.toFile();
		return new FileSystemResource(file);
	}

	/**
	 * @param task
	 * @return
	 */
	public String getGraphMLTaskColor(Task task) {

		String color = Constants.GRAPH_ML_COLOR_BLACK_DEFAULT;
		String type = activityType.get(task.getActivityType());

		if (graphMlTaskColors.containsKey(type)) {
			color = graphMlTaskColors.get(type);
		}
		return color;
	}

}
