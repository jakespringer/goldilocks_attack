package edu.mit.csail.alfagroup.renamevariable;

import com.github.javaparser.*;
import com.github.javaparser.ast.*;
import com.github.javaparser.ast.body.*;
import com.github.javaparser.ast.expr.*;
import com.github.javaparser.utils.*;

import java.io.*;
import java.util.*;
import java.util.stream.*;
import java.nio.file.*;

public class RenameVariable {
    private enum PerturbationType {
        SINGLE, SAME, DIFFERENT
    }

    private static Random random = new Random();
    private static List<String> dictionary;
    private static PerturbationType perturbationType;
    
    private static String toCamelCase(List<String> strings) {
        return strings.stream()
		.map(s -> s.toLowerCase())
		.map(s -> s.substring(0, 1).toUpperCase() + s.substring(1).toLowerCase())
		.collect(Collectors.joining()); 
    }

    private static void replaceLocalVariable(VariableDeclarator e, String toReplace, String toReplaceWith) {
        if (e.getName().asString().equals(toReplace)) {
            e.setName(new SimpleName(toReplaceWith));
	}
    }

    private static void replaceLocalVariable(Parameter e, String toReplace, String toReplaceWith) {
        if (e.getName().asString().equals(toReplace)) {
            e.setName(new SimpleName(toReplaceWith));
	}
    }

    private static void replaceLocalVariable(NameExpr e, String toReplace, String toReplaceWith) {
        if (e.getName().asString().equals(toReplace)) {
            e.setName(new SimpleName(toReplaceWith));
	}
    }

    private static void perturbMethodDeclaration(MethodDeclaration method) {
	String perturbedWord = "";
	switch (perturbationType) {
        case SINGLE:
	    perturbedWord = dictionary.get(random.nextInt(dictionary.size()));
	    break;
	case SAME:
	    String perturbedWordSubtoken = dictionary.get(random.nextInt(dictionary.size()));
	    List<String> subtokens = Arrays.asList(perturbedWordSubtoken, perturbedWordSubtoken, perturbedWordSubtoken, perturbedWordSubtoken, perturbedWordSubtoken);
            perturbedWord = toCamelCase(subtokens);
            break;
	case DIFFERENT:
            List<String> words = new ArrayList<>();
	    for (int i=0; i<5; ++i) {
                words.add(dictionary.get(random.nextInt(dictionary.size())));
	    }
	    perturbedWord = toCamelCase(words);
	    break;
	}

	final String replacement = perturbedWord;
	List<String> localVarNames = new ArrayList<>();
	method.walk(VariableDeclarator.class, e -> localVarNames.add(e.getName().asString()));
	method.walk(Parameter.class, e -> localVarNames.add(e.getName().asString()));
	if (localVarNames.size() > 0) {
	    String selectedVariable = localVarNames.get(random.nextInt(localVarNames.size()));
	    method.walk(VariableDeclarator.class, e -> replaceLocalVariable(e, selectedVariable, replacement));
	    method.walk(Parameter.class, e -> replaceLocalVariable(e, selectedVariable, replacement));
	    method.walk(NameExpr.class, e -> replaceLocalVariable(e, selectedVariable, replacement));
	}
    }

    public static void main(String[] args) throws Exception {
	if (args.length != 3) {
            System.err.println("RenameVariable: [dictionary] [input file] [single|same|different]");
	    System.exit(1);
	}

	if (args[2].equals("single")) {
            perturbationType = PerturbationType.SINGLE;
	} else if (args[2].equals("same")) {
            perturbationType = PerturbationType.SAME;
	} else if (args[2].equals("different")) {
            perturbationType = PerturbationType.DIFFERENT;
	} else {
            System.err.println("RenameVariable: error, third argument must be one of [single|same|different]");
	}

	dictionary = Files.readAllLines(Paths.get(args[0]));
        CompilationUnit cu = StaticJavaParser.parse(new File(args[1])); 
	cu.walk(MethodDeclaration.class, m -> perturbMethodDeclaration(m));
	System.out.println(cu);
    }
}

