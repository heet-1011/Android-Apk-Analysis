Java.perform(function () {
    console.log("[*] Universal API Logger - Frida Hook Loaded.");

    var loadedClasses = Java.enumerateLoadedClassesSync();
    var totalHooked = 0;
    var totalSkipped = 0;

    loadedClasses.forEach(function (className) {
        try {
            var targetClass = Java.use(className);
            var methods = targetClass.class.getDeclaredMethods();

            methods.forEach(function (method) {
                try {
                    var methodName = method.getName();

                    if (!targetClass[methodName]) {
                        //console.log("[-] Skipping: " + className + "." + methodName + " (No overloads)");
                        totalSkipped++;
                        return;
                    }

                    targetClass[methodName].overloads.forEach(function (overload) {
                        overload.implementation = function () {
                            var logMessage = {
                                "Class": className,
                                "Method": methodName,
                                "Arguments": []
                            };

                            for (var i = 0; i < arguments.length; i++) {
                                logMessage.Arguments.push(arguments[i].toString());
                            }

                            var result = overload.apply(this, arguments);
                            logMessage["Return"] = result ? result.toString() : "null";

                            // console.log("[+] Hooked: " + className + "." + methodName);
                            send(logMessage);
                            return result;
                        };

                        totalHooked++;
                    });

                } catch (err) {
                    console.log("[-] Error Hooking " + className + "." + method.getName() + ": " + err);
                }
            });

        } catch (err) {
            console.log("[-] Error Processing Class " + className + ": " + err);
        }
    });

    // console.log("\n[*] Java API Logging Active.");
    // console.log("[*] Total Methods Hooked: " + totalHooked);
    // console.log("[*] Total Methods Skipped: " + totalSkipped);
});

